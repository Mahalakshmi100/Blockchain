import hashlib
import json
import time
import re  # for voter ID validation


class Block:
    def __init__(self, index, timestamp, data, previous_hash):
        self.index = index
        self.timestamp = timestamp
        self.data = data
        self.previous_hash = previous_hash
        self.hash = self.calculate_hash()

    def calculate_hash(self):
        block_string = f"{self.index}{self.timestamp}{json.dumps(self.data)}{self.previous_hash}"
        return hashlib.sha256(block_string.encode()).hexdigest()


class Blockchain:
    def __init__(self):
        self.chain = [self.create_genesis_block()]

    def create_genesis_block(self):
        return Block(0, time.ctime(), {"Genesis Block": "First Block"}, "0")

    def get_latest_block(self):
        return self.chain[-1]

    def add_block(self, new_block):
        new_block.previous_hash = self.get_latest_block().hash
        new_block.hash = new_block.calculate_hash()
        self.chain.append(new_block)


class VotingSystem:
    def __init__(self):
        self.blockchain = Blockchain()
        self.voted_ids = set()
        # Candidate symbols
        self.candidates = {"@": "Dinesh", "#": "Seetha", "$": "Rahul"}
        self.exit_symbol = "."

    def is_valid_voter_id(self, voter_id):
        """Validate voter ID format (V followed by 3 digits)."""
        return re.fullmatch(r"V\d{3}", voter_id) is not None

    def cast_vote(self, voter_id, name, symbol):
        if voter_id in self.voted_ids:
            print(f"❌ Invalid Vote! Voter ID {voter_id} has already voted.\n")
            return False

        if symbol not in self.candidates:
            print("❌ Invalid Symbol! Vote not counted.\n")
            return False

        vote_data = {
            "VoterID": voter_id,
            "Name": name,
            "Vote": self.candidates[symbol],
            "Symbol": symbol
        }

        new_block = Block(len(self.blockchain.chain),
                          time.ctime(),
                          vote_data,
                          self.blockchain.get_latest_block().hash)
        self.blockchain.add_block(new_block)
        self.voted_ids.add(voter_id)

        print(f"✅ Vote recorded successfully for {self.candidates[symbol]} ({symbol}) by {name} (ID: {voter_id})\n")
        return True

    def display_results(self):
        print("\n📊 Final Vote Count:")
        vote_count = {candidate: 0 for candidate in self.candidates.values()}

        for block in self.blockchain.chain[1:]:  # skip genesis block
            vote_count[block.data["Vote"]] += 1

        for candidate, count in vote_count.items():
            symbol = [sym for sym, name in self.candidates.items() if name == candidate][0]
            print(f"{candidate} ({symbol}): {count}")

        winner = max(vote_count, key=vote_count.get)
        max_votes = max(vote_count.values())

        # Check for tie
        if list(vote_count.values()).count(max_votes) > 1:
            print("🎉 It's a Tie!")
        else:
            print(f"🏆 Winner: {winner} 🎉")

    def display_blockchain(self):
        print("\n⛓️ Blockchain Ledger:")
        for block in self.blockchain.chain:
            print(f"Index: {block.index}")
            print(f"Timestamp: {block.timestamp}")
            print(f"Data: {block.data}")
            print(f"Hash: {block.hash[:20]}...")  # shorten hash
            print(f"Previous Hash: {block.previous_hash[:20]}...\n")


if __name__ == "__main__":
    voting = VotingSystem()
    print("🗳️ Welcome to Secure Blockchain Voting System (Symbol-based)\n")
    print("🔐 Candidate Symbol Mapping:")
    for symbol, candidate in voting.candidates.items():
        print(f"Symbol: {symbol} → Candidate: {candidate}")
    print(f"Symbol: {voting.exit_symbol} → Exit voting\n")

    while True:
        voter_id = input("Enter your Voter ID (or '.' to exit): ").strip()

        if voter_id.lower() == voting.exit_symbol:
            print("👋 Exiting voting session.")
            break

        if not voting.is_valid_voter_id(voter_id):
            print("❌ Invalid Voter ID format! Must be like 'V101'.\n")
            continue

        name = input("Enter your Name: ").strip()
        print(f"Available Symbols: {list(voting.candidates.keys()) + [voting.exit_symbol]}")
        symbol = input("Enter the symbol of your chosen candidate: ").strip()

        if symbol == voting.exit_symbol:
            print("👋 Exiting voting session.")
            break

        voting.cast_vote(voter_id, name, symbol)

    voting.display_results()
    voting.display_blockchain()
