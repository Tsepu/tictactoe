import sys
from collections import deque
from PyQt5 import QtWidgets as qw

class XO:
    def __init__(self):
        self.check_ndxes = [
            [0,1,2],[3,4,5],[6,7,8],[0,3,6],[1,4,7],[2,5,8],[0,4,8],[2,4,6]
        ]
        self.restart()
    
    def __str__(self) -> str:
        return f"""
        X: {self.x_pos}\n
        O: {self.o_pos}\n
        Next: {self.player}
        """
    
    def restart(self):
        
        self.player = 'X'
        self.winner_ndxes = []
        self.x_pos = deque(maxlen=3)
        self.o_pos = deque(maxlen=3)
        
    def check_winner(self):
        
        result = list(self.x_pos) if self.player == 'X' else list(self.o_pos)
        result = sorted(result)
        
        if len(result) == 3:
        
            for ndxes in self.check_ndxes:
                if result == ndxes:
                    self.winner_ndxes = ndxes
                    return True
            
            if self.player == 'X':
                self.x_pos.popleft()
            
            elif self.player == 'O':
                self.o_pos.popleft()

            
        
        self.player = 'X' if self.player == 'O' else 'O'
        return False
            
    def play(self, ndx):
        if self.player == 'X' and ndx not in self.o_pos:
            self.x_pos.append(ndx)
            return True
        
        if self.player == 'O' and ndx not in self.x_pos:
            self.o_pos.append(ndx)
            return True
        
        return False
        
class XOGui(qw.QWidget):
    def __init__(self):
        super().__init__()
        
        self.game = XO()
        self.finished = False
        
        self.setWindowTitle("Tic-Tac-Toe")
        self.setGeometry(0, 0, 350, 400)
        self.setFixedSize(350, 400)
        
        grid_layout = qw.QGridLayout()
        grid_layout.setContentsMargins(0, 0, 0, 0)
        
        self.buttons = []
        for i in range(9):
            row = i // 3
            col = i % 3
            
            btn =  qw.QPushButton("", self)
            btn.setFixedSize(100, 100)
            btn.setProperty("ndx", i)
            
            btn.clicked.connect(self.on_btn_play)
            self.buttons.append(btn)
            grid_layout.addWidget(btn, row, col)
            
        
        btn_start = qw.QPushButton("Start Game", self)
        btn_start.setFixedSize(320, 30)
        btn_start.setStyleSheet("background-color: lightblue; font-size: 20px;")
        btn_start.clicked.connect(self.on_btn_start)
        
        self.player = qw.QLabel(f"Player: {self.game.player}")
        self.player.setStyleSheet("font-size: 20px;")
        
        
        main_layout = qw.QVBoxLayout()
        
        main_layout.addWidget(self.player )
        main_layout.addLayout(grid_layout)
        main_layout.addWidget(btn_start)
        
        self.setLayout(main_layout)
        
        

    def on_btn_start(self):
        self.game.restart()
        self.finished = False
        
        self.check_buttons()
    
    def on_btn_play(self):
        if self.finished:
            self.game.restart()
            self.finished = False
            
        
        sender_btn = self.sender()
        ndx = sender_btn.property("ndx")
        
        valid = self.game.play(ndx)
        
        if valid:
            win = self.game.check_winner()
            
            if win:
                self.finished = True
        
        self.check_buttons()
        
    def check_buttons(self):
        
        for ndx, btn in enumerate(self.buttons):
            btn.setStyleSheet("background-color: none;  font-size: 30px;")
            
            if ndx in self.game.x_pos:
                btn.setText("X")
            elif ndx in self.game.o_pos:
                btn.setText("O")
            else:
                btn.setText("")
        
        if self.finished:
            for ndx in self.game.winner_ndxes:
                self.buttons[ndx].setStyleSheet("background-color: green;  font-size: 30px;")
        
        else:
            self.player.setText(f"Player {self.game.player}")
        
         
if __name__ == '__main__':
    app = qw.QApplication(sys.argv)
    gui = XOGui()
    
    gui.show()
    sys.exit(app.exec_())
