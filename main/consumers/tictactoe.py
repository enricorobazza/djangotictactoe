import json
from channels.generic.websocket import AsyncWebsocketConsumer
from main.logic.game import Game

class TicTacToeConsumer(AsyncWebsocketConsumer):
    games = {}

    @property
    def game(self):
        return self.games[self.room_name]

    @classmethod
    def add_player(cls, room_name, player):
        if room_name not in cls.games:
            cls.games[room_name] = Game()

        return cls.games[room_name].add_player(player)


    @classmethod
    def remove_player(cls, room_name, player):
        if room_name not in cls.games:
            return
        cls.games[room_name].remove_player(player)
        if len(cls.games[room_name].players) == 0:
            cls.games.pop(room_name, None)
        

    async def notify_other_user_left(self):
        other_player = self.game.get_other_player(self.unique_id)

        await self.channel_layer.group_send(
                'user_%s'%other_player,
                {
                    'type': 'status_message',
                    'connect': False,
                    'message': 'Outro jogador desconectou'
                }
            )
    

    async def send_user_message(self, message, user=None):
        if user is None:
            user = self.unique_id

        await self.channel_layer.group_send(
            'user_%s'%user,
            message
        )

    async def connect(self):
        self.room_name = self.scope['url_route']['kwargs']['room_name']
        self.unique_id = self.scope['url_route']['kwargs']['unique_id']

        self.room_group_name = 'tictactoe_%s' % self.room_name

        can_add = TicTacToeConsumer.add_player(self.room_name, self.unique_id)

        if(can_add):
        # Join room group
            print("Player joined %s: %s"%(self.room_name, self.unique_id))
            await self.channel_layer.group_add(
                self.room_group_name,
                self.channel_name
            )
            await self.send_user_message({
                    'type': 'status_message',
                    'connect': True,
                })
            await self.send_user_message({
                    'type': 'initial_game_status',
                    'status': self.game.status(self.unique_id)
                })

        else:
            await self.channel_layer.group_send(
                'user_%s'%self.unique_id,
                {
                    'type': 'status_message',
                    'connect': False,
                    'message': 'Sala cheia'
                }
            )

        await self.accept()
        

    async def disconnect(self, close_code):
        # Leave room group

        await self.notify_other_user_left()
        TicTacToeConsumer.remove_player(self.room_name, self.unique_id)
        
        print("Player leaving %s: %s"%(self.room_name, self.unique_id))

        await self.channel_layer.group_discard(
            self.room_group_name,
            self.channel_name
        )

    # Receive message from WebSocket
    async def receive(self, text_data):
        text_data_json = json.loads(text_data)
        if 'i' in text_data_json and 'j' in text_data_json:
            i = text_data_json['i']
            j = text_data_json['j']
            self.game.make_move(self.unique_id, i, j)

        elif 'reset' in text_data_json and text_data_json['reset'] == True:
            self.game.reset()

            # Send message to room group
        await self.channel_layer.group_send(
            self.room_group_name,
            {
                'type': 'game_status',
            }
        )
        

    # Receive message from room group
    async def game_status(self, event):
        await self.send(text_data=json.dumps({
            'status': self.game.status(self.unique_id)
        }))