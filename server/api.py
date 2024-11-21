from flask import Flask, request, jsonify

from arena import Arena
from character import Character, Statistics

from actions import Action, ActionType

class API:
  def __init__(self, arena: Arena):
    self.app = Flask(__name__)

    @self.app.route('/')
    def index():
      return "Arena"
    
    @self.app.route('/state', methods=['GET'])
    def get_current_state():
      return jsonify(arena.__dict__)
    
    @self.app.route('/characters', methods=['GET'])
    def get_characters():
      return jsonify(arena.characters)

    @self.app.route('/characters/<character_id>', methods=['GET'])
    def get_character(character_id: int):
      character = arena.get_character(character_id)
      return jsonify(character)
    
    @self.app.route('/characters/<character_id>/join', methods=['POST'])
    def character_join(character_id: int):
      data = request.json

      id = character_id

      life = data['life']
      strength = data['strength']
      armor = data['armor']
      speed = data['speed']

      statistics = Statistics(life, strength, armor, speed)
      character = Character(id, statistics)

      arena.add_character(character)

      return True

    @self.app.route('/characters/<character_id>/action', methods=['POST'])
    def character_action(character_id: int):
      data = request.json

      character = arena.get_character(character_id)

      type = data['type']
      target = data['target']

      actionType = ActionType.from_str(type)
      action = Action(actionType, character_id, target)

      character.prepare_action(action)

  def start(self):
    self.app.run()