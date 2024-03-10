import os
from dotenv import load_dotenv
from betfairlightweight import APIClient, filters

from bot.bot_logic import ArbitrageBettingStrategy, EachWayBettingStrategy, LayBettingStrategy

class BettingStrategy:
    def __init__(self, strategy_name, parameters=None):
        self.strategy_name = strategy_name
        self.parameters = parameters or {}
        self.client = self.initialize_api_client()

    def initialize_api_client(self):
        load_dotenv()
        username = os.getenv("BETFAIR_USERNAME")
        password = os.getenv("BETFAIR_PASSWORD")
        app_key = os.getenv("BETFAIR_APP_KEY")
        cert_path = os.getenv("BETFAIR_CERT_PATH")
        key_path = os.getenv("BETFAIR_KEY_PATH")

        if username and password and app_key and cert_path and key_path:
            client = APIClient(username, password, app_key=app_key, cert_files=(cert_path, key_path))
            client.login()
            return client
        else:
            raise ValueError("Missing Betfair API credentials. Please check your environment variables.")

    def execute(self, market_id):
        raise NotImplementedError("Subclasses must implement the execute method.")

    def get_market_data(self, market_id):
        market_book = self.client.betting.list_market_book(
            market_ids=[market_id],
            price_projection=filters.price_projection(price_data=["EX_BEST_OFFERS"]),
            order_projection="ALL",
            match_projection="ROLLED_UP_BY_PRICE"
        )

        if market_book:
            return market_book[0]
        else:
            return None

    def place_bet(self, market_id, selection_id, stake, odds, side="BACK"):
        price = self.client.betting.price_size_to_price(odds)
        instruction = filters.place_instruction(selection_id=selection_id, side=side, order_type="LIMIT", 
                                                 size_taken=stake, price=price)
        order = self.client.betting.place_orders(market_id=market_id, instructions=[instruction])
        if order:
            print(f"Bet placed successfully. Order ID: {order[0]['instructionReports'][0]['betId']}")
        else:
            print("Failed to place bet.")


class MartingaleStrategy(BettingStrategy):
    def __init__(self, initial_bet, max_bet, max_consecutive_losses):
        super().__init__("Martingale", {
            "initial_bet": initial_bet,
            "max_bet": max_bet,
            "max_consecutive_losses": max_consecutive_losses
        })
        self.current_bet = initial_bet
        self.consecutive_losses = 0

    def execute(self, market_id):
        market_data = self.get_market_data(market_id)
        if market_data:
            selection_id, odds = self.get_best_selection(market_data)
            if selection_id and odds:
                if self.should_place_bet(odds):
                    self.place_bet(market_id, selection_id, self.current_bet, odds)
                    if self.did_win(market_data, selection_id):
                        print(f"Congratulations! You won ${self.current_bet}!")
                        self.current_bet = self.parameters["initial_bet"]
                        self.consecutive_losses = 0
                    else:
                        print(f"Oops! You lost ${self.current_bet}.")
                        self.current_bet = min(self.current_bet * 2, self.parameters["max_bet"])
                        self.consecutive_losses += 1
                        if self.consecutive_losses >= self.parameters["max_consecutive_losses"]:
                            print(f"Reached maximum consecutive losses. Resetting to initial bet.")
                            self.current_bet = self.parameters["initial_bet"]
                            self.consecutive_losses = 0
                else:
                    print("Odds not favorable. Skipping this race.")
            else:
                print("No suitable selection found. Skipping this race.")
        else:
            print("Failed to retrieve market data. Skipping this race.")

    def get_best_selection(self, market_data):
        # Implement your logic to select the best horse based on the market data
        # Example: Select the horse with the highest odds
        best_selection = None
        best_odds = 0
        for runner in market_data.runners:
            if runner.status == "ACTIVE" and runner.ex.available_to_back:
                odds = runner.ex.available_to_back[0].price
                if odds > best_odds:
                    best_selection = runner.selection_id
                    best_odds = odds
        return best_selection, best_odds

    def should_place_bet(self, odds):
        # Implement your logic to determine if the bet should be placed based on the odds
        # Example: Place bet if odds are greater than or equal to 2.0
        return odds >= 2.0

    def did_win(self, market_data, selection_id):
        # Implement your logic to determine if the bet won based on the market data
        # Example: Check if the selected horse is the winner
        for runner in market_data.runners:
            if runner.selection_id == selection_id and runner.status == "WINNER":
                return True
        return False


class ValueBettingStrategy(BettingStrategy):
    def __init__(self, initial_bet, max_bet, value_threshold):
        super().__init__("ValueBetting", {
            "initial_bet": initial_bet,
            "max_bet": max_bet,
            "value_threshold": value_threshold
        })

    def execute(self, market_id):
        market_data = self.get_market_data(market_id)
        if market_data:
            selection_id, odds = self.find_value_bet(market_data)
            if selection_id and odds:
                stake = self.calculate_stake(odds)
                self.place_bet(market_id, selection_id, stake, odds)
                print(f"Placed a value bet on selection {selection_id} with odds {odds} and stake {stake}")
            else:
                print("No value bet found. Skipping this race.")
        else:
            print("Failed to retrieve market data. Skipping this race.")

    def find_value_bet(self, market_data):
        # Implement your logic to find a value bet based on the market data
        # Example: Compare estimated probability with actual odds
        for runner in market_data.runners:
            if runner.status == "ACTIVE" and runner.ex.available_to_back:
                odds = runner.ex.available_to_back[0].price
                estimated_probability = self.calculate_estimated_probability(runner)
                if odds > 1 / (estimated_probability + self.parameters["value_threshold"]):
                    return runner.selection_id, odds
        return None, None

    def calculate_estimated_probability(self, runner):
        # Implement your logic to estimate the probability of winning for a given runner
        # Example: Use a simple scoring system based on runner attributes
        score = 0
        if runner.last_10_form:
            score += runner.last_10_form.count("1") * 3
            score += runner.last_10_form.count("2") * 2
            score += runner.last_10_form.count("3")
        if runner.handicap < 10:
            score += 5
        elif runner.handicap < 20:
            score += 3
        if runner.days_since_last_run < 30:
            score += 2
        return score / 100

    def calculate_stake(self, odds):
        # Implement your logic to calculate the stake based on the odds and your betting strategy
        # Example: Use a fixed percentage of the maximum bet amount
        return self.parameters["max_bet"] * 0.05
    
    class EachWayBettingStrategy(BettingStrategy):
        def __init__(self, initial_bet, max_bet, place_terms):
            super().__init__("EachWayBetting", {
            "initial_bet": initial_bet,
            "max_bet": max_bet,
            "place_terms": place_terms
        })

    def execute(self, market_id):
        market_data = self.get_market_data(market_id)
        if market_data:
            selection_id, odds = self.find_best_selection(market_data)
            if selection_id and odds:
                win_stake, place_stake = self.calculate_stakes(odds)
                self.place_bet(market_id, selection_id, win_stake, odds, side="BACK")
                self.place_bet(market_id, selection_id, place_stake, self.calculate_place_odds(odds), side="BACK")
                print(f"Placed an each-way bet on selection {selection_id} with odds {odds}")
            else:
                print("No suitable selection found for each-way betting. Skipping this race.")
        else:
            print("Failed to retrieve market data. Skipping this race.")

    def find_best_selection(self, market_data):
        # Implement your logic to find the best selection for each-way betting
        # Example: Select the horse with the highest odds within a certain range
        min_odds = 5.0
        max_odds = 10.0
        best_selection = None
        best_odds = 0
        for runner in market_data.runners:
            if runner.status == "ACTIVE" and runner.ex.available_to_back:
                odds = runner.ex.available_to_back[0].price
                if min_odds <= odds <= max_odds and odds > best_odds:
                    best_selection = runner.selection_id
                    best_odds = odds
        return best_selection, best_odds

    def calculate_stakes(self, odds):
        # Calculate the win and place stakes based on the odds and betting strategy
        # Example: Allocate a portion of the total stake to win and place bets
        total_stake = self.parameters["initial_bet"]
        win_stake = total_stake * 0.7
        place_stake = total_stake * 0.3
        return win_stake, place_stake

    def calculate_place_odds(self, win_odds):
        # Calculate the place odds based on the win odds and place terms
        # Example: Use a fixed place terms of 1/4 odds for top 3 places
        place_terms = self.parameters["place_terms"]
        return (win_odds - 1) * place_terms + 1
    
    class ArbitrageBettingStrategy(BettingStrategy):
    
        def __init__(self, stake_percentage):
            super().__init__("ArbitrageBetting", {
            "stake_percentage": stake_percentage
        })

    def execute(self, market_id):
        market_data = self.get_market_data(market_id)
        if market_data:
            arbitrage_opportunity = self.find_arbitrage_opportunity(market_data)
            if arbitrage_opportunity:
                selection_id, back_odds, lay_odds = arbitrage_opportunity
                stake = self.calculate_stake(back_odds, lay_odds)
                self.place_bet(market_id, selection_id, stake, back_odds, side="BACK")
                self.place_bet(market_id, selection_id, stake, lay_odds, side="LAY")
                print(f"Placed an arbitrage bet on selection {selection_id} with back odds {back_odds} and lay odds {lay_odds}")
            else:
                print("No arbitrage opportunity found. Skipping this race.")
        else:
            print("Failed to retrieve market data. Skipping this race.")

    def find_arbitrage_opportunity(self, market_data):
        # Implement your logic to find an arbitrage opportunity in the market
        # Example: Compare back and lay odds to find a profitable arbitrage
        for runner in market_data.runners:
            if runner.status == "ACTIVE" and runner.ex.available_to_back and runner.ex.available_to_lay:
                back_odds = runner.ex.available_to_back[0].price
                lay_odds = runner.ex.available_to_lay[0].price
                if back_odds > lay_odds:
                    return runner.selection_id, back_odds, lay_odds
        return None

    def calculate_stake(self, back_odds, lay_odds):
        # Calculate the stake for the arbitrage bet based on the odds
        # Example: Use a fixed percentage of the available balance
        return self.client.account.get_account_funds()["available_to_bet"] * self.parameters["stake_percentage"]
    
    class LayBettingStrategy(BettingStrategy):
        def __init__(self, initial_bet, max_bet, min_odds):
            super().__init__("LayBetting", {
            "initial_bet": initial_bet,
            "max_bet": max_bet,
            "min_odds": min_odds
        })

    def execute(self, market_id):
        market_data = self.get_market_data(market_id)
        if market_data:
            selection_id, odds = self.find_lay_bet(market_data)
            if selection_id and odds:
                stake = self.calculate_stake(odds)
                self.place_bet(market_id, selection_id, stake, odds, side="LAY")
                print(f"Placed a lay bet on selection {selection_id} with odds {odds} and stake {stake}")
            else:
                print("No suitable lay betting opportunity found. Skipping this race.")
        else:
            print("Failed to retrieve market data. Skipping this race.")

    def find_lay_bet(self, market_data):
        # Implement your logic to find a lay betting opportunity in the market
        # Example: Find a selection with odds above a certain threshold
        min_odds = self.parameters["min_odds"]
        for runner in market_data.runners:
            if runner.status == "ACTIVE" and runner.ex.available_to_lay:
                odds = runner.ex.available_to_lay[0].price
                if odds >= min_odds:
                    return runner.selection_id, odds
        return None, None

    def calculate_stake(self, odds):
        # Calculate the stake for the lay bet based on the odds and betting strategy
        # Example: Use a fixed percentage of the maximum bet amount
        return self.parameters["max_bet"] * 0.05
    
    # Example usage
if __name__ == "__main__":
    load_dotenv()
    market_id = os.getenv("MARKET_ID")

    martingale_strategy = MartingaleStrategy(initial_bet=10, max_bet=100, max_consecutive_losses=5)
    martingale_strategy.execute(market_id)

    value_betting_strategy = ValueBettingStrategy(initial_bet=10, max_bet=100, value_threshold=0.05)
    value_betting_strategy.execute(market_id)

    each_way_strategy = EachWayBettingStrategy(initial_bet=10, max_bet=100, place_terms=0.25)
    each_way_strategy.execute(market_id)

    arbitrage_strategy = ArbitrageBettingStrategy(stake_percentage=0.02)
    arbitrage_strategy.execute(market_id)

    lay_betting_strategy = LayBettingStrategy(initial_bet=10, max_bet=100, min_odds=3.0)
    lay_betting_strategy.execute(market_id)