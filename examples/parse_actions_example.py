"""
Example usage of the Actions parser.

Demonstrates how to parse actions from a decompressed HBR2 data stream.
"""

from haxmetrics.binary_reader import BinaryReader
from haxmetrics.models.actions import Actions, ActionType

# Example: Parse actions from decompressed data
def parse_actions_example():
    """
    Example of parsing actions from decompressed HBR2 data.
    
    In a real scenario, you would:
    1. Read the HBR2 file header
    2. Decompress the data section
    3. Parse messages, room state, and game state
    4. Then parse actions from the remaining data
    """
    # Simulated decompressed actions data
    # This would normally come from decompressing the HBR2 file
    actions_data = bytes([
        # Action 1: MatchStart (Type 7)
        # frame_delta=10, sender=0, type=7
        10, 0, 0, 7,
        
        # Action 2: PlayerInput (Type 3) - kick pressed
        # frame_delta=5, sender=1, type=3, input=0x0010 (kick bit)
        5, 0, 1, 3, 0x00, 0x10,
        
        # Action 3: MatchStopped (Type 8)
        # frame_delta=300, sender=0, type=8
        0xAC, 0x02, 0, 0, 8,
    ])
    
    reader = BinaryReader(actions_data)
    actions = Actions.parse(reader)
    
    print(f"Total actions parsed: {len(actions)}")
    print()
    
    # Iterate over all actions
    for i, action in enumerate(actions):
        print(f"Action {i+1}:")
        print(f"  Type: {action.action_type.name}")
        print(f"  Frame delta: {action.frame_delta}")
        print(f"  Sender: {action.sender}")
        print(f"  Data: {action.to_dict()}")
        print()
    
    # Get absolute frame numbers
    absolute_frames = actions.get_absolute_frames()
    print(f"Absolute frames: {absolute_frames}")
    print()
    
    # Filter actions by type
    input_actions = actions.filter_by_type(ActionType.PLAYER_INPUT)
    print(f"Player input actions: {len(input_actions)}")
    if input_actions:
        for action in input_actions:
            print(f"  Input: 0x{action.input:04x}")
            print(f"  Is kick: {action.is_kick}")
    print()
    
    # Filter actions by sender
    system_actions = actions.filter_by_sender(0)
    print(f"System actions (sender=0): {len(system_actions)}")
    for action in system_actions:
        print(f"  - {action.action_type.name}")


if __name__ == "__main__":
    parse_actions_example()
