#-*- coding: utf-8 -*-

import sys, pygame, copy, os
from minimax import *
from abc import *
from math import *
from myMenu import MenuItem, Text, Button
from pygame.locals import *

global DONE
global BOARD_MAP
global RED_DEFAULT,     RED_DEFAULT_SELECTED
global RED_CHECKER,     RED_CHECKER_SELECTED
global BLACK_DEFAULT, BLACK_DEFAULT_SELECTED
global BLACK_CHECKER, BLACK_CHECKER_SELECTED
global CAPTURE_MODE, CAPTURE_LIST, CAPTURE_COUNT


def printBoardMap():
	for i in BOARD_MAP:
		print i


class Checkers(object):
	def __init__(self,screen, file_name = "images/board11.png"):
		global BOARD_MAP, DONE, GAME_TEXT
		global RED_DEFAULT,     RED_DEFAULT_SELECTED
		global RED_CHECKER,     RED_CHECKER_SELECTED
		global BLACK_DEFAULT, BLACK_DEFAULT_SELECTED
		global BLACK_CHECKER, BLACK_CHECKER_SELECTED
		global CAPTURE_MODE, CAPTURE_LIST, CAPTURE_COUNT
		
		
		RED_DEFAULT				= pygame.image.load("images/red_default.png"           ).convert_alpha()
		RED_DEFAULT_SELECTED	= pygame.image.load("images/red_default_selected.png"  ).convert_alpha()
		RED_CHECKER				= pygame.image.load("images/red_checker.png"           ).convert_alpha()
		RED_CHECKER_SELECTED	= pygame.image.load("images/red_checker_selected.png"  ).convert_alpha()
		
		BLACK_DEFAULT 			= pygame.image.load("images/black_default.png"         ).convert_alpha()
		BLACK_DEFAULT_SELECTED	= pygame.image.load("images/black_default_selected.png").convert_alpha()
		BLACK_CHECKER			= pygame.image.load("images/black_checker.png"         ).convert_alpha()
		BLACK_CHECKER_SELECTED	= pygame.image.load("images/black_checker_selected.png").convert_alpha()
		
		CAPTURE_MODE  = False
		CAPTURE_LIST  = []
		CAPTURE_COUNT = 0
		
		
		BOARD_MAP = [['#','b','#','b','#','b','#','b'],		# (r) - red piece
					 ['b','#','b','#','b','#','b','#'],		# (b) - black piece
					 ['#','b','#','b','#','b','#','b'],		# (#) - unplayable slot
					 ['.','#','.','#','.','#','.','#'],		# (.) - free slot
					 ['#','.','#','.','#','.','#','.'],		# (R) - red checker piece
					 ['r','#','r','#','r','#','r','#'],		# (B) - black checker piece
					 ['#','r','#','r','#','r','#','r'],
					 ['r','#','r','#','r','#','r','#']]
		
		self.screen = screen
		
		self.RED_TURN = True
		
		self.board_image = pygame.image.load(file_name).convert()
		self.red_pieces = []
		self.black_pieces = []
		self.selected_piece = None	# Set the selected piece
		
		self.TILE_X = self.board_image.get_size()[0]/8 		# number of pixels on x
		self.TILE_Y = self.board_image.get_size()[0]/8 		# number of pixels on y
		
		# Start the pieces on board
		for row in range(len(BOARD_MAP)):
			for col in range(len(BOARD_MAP[0])):
				if BOARD_MAP[row][col] == 'r':
					p = RedPiece((row,col))
					self.red_pieces.append(p)
					
				if BOARD_MAP[row][col] == 'b':
					p = BlackPiece((row,col))
					self.black_pieces.append(p)
				
				if BOARD_MAP[row][col] == 'R':										# <<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<
					p = RedPiece((row,col))											# remover esta parte após conclusão
					p.promote()
					self.red_pieces.append(p)
				if BOARD_MAP[row][col] == 'x':
					p = BlackPiece((row,col))
					self.black_pieces.append(p)
					CAPTURE_LIST.append(p)
				if BOARD_MAP[row][col] == 'B':
					p = BlackPiece((row,col))
					p.promote()
					self.black_pieces.append(p)										# <<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<
		
		self.font = pygame.font.Font("data/FEASFBRG.TTF",32)
		self.create_itens()
	
	
	def create_itens(self):
		global GAME_TEXT
		self.itens = []
		self.buttons = []
		new = [("Menu",     6),
		       ('',      None)]
		
		itens_height = 0
		for n in new:
			if n[1] == None:
				new_item = Text(n[0])
				GAME_TEXT = new_item
			else:
				new_item = Button(n[0],n[1])
				self.buttons.append(new_item)
			
			width, height = self.font.size(n[0])				# Pega o tamanho ocupado pelo texto
			itens_height += height
			
			new_item.rect = pygame.Rect((0,0),(width, height))	# Cria a área ocupada pelo botão
			
			self.itens.append(new_item)
		
		# define as posições dos botões na região cinza abaixo do tabuleiro
		board_width,board_height = self.TILE_X*8, self.TILE_Y*8
		image_width,image_height = self.board_image.get_size()
		height_position = board_height + (image_height - board_height)/2
		width_position = image_width
		
		#for b in self.itens:
			#width_position -= b.rect.width/2 + 5
			#b.center_position(width_position,height_position)
			#width_position -= b.rect.width/2
		
		b = self.itens[0]
		b.center_position(self.TILE_X*7,self.TILE_Y*8.5)
		
		b = self.itens[1]
		b.center_position(0,self.TILE_Y*8.5)
		
	
	
	#
	def start_checkers(self, minimax_depth=None):
		global DONE, GAME_TEXT
		
		self.__init__(self.screen)
		self.screen = pygame.display.set_mode(self.board_image.get_size(),RESIZABLE,32)
		
		if minimax_depth:
			mm = Decisao_Alfa_Beta(minimax_depth,self)
		
		done = False
		DONE = False
		while not done and not DONE:
			
			self.screen.fill((0,0,0))
			self.screen.blit(self.board_image,(0,0))
			
			if self.RED_TURN:
				GAME_TEXT.update_text("Vermelhas Jogam")
			else:
				GAME_TEXT.update_text("Pretas Jogam")
				self.update(self.screen)
				pygame.display.flip()
			
			if minimax_depth and not self.RED_TURN:
				print "START MINIMAX"
				estado_minimax = Estado(self.red_pieces,self.black_pieces,BOARD_MAP)
				
				j,v = mm.comecar(estado_minimax,estado_minimax.pretas,estado_minimax.vermelhas)
				print "preto jogou",j.pos_inicial, "para",j.pos_final,'por',v
				
				print j,v
				
				self.play(j)
				self.RED_TURN = True
			
			self.events()
			self.update(self.screen)
			done = self.end_of_game(BOARD_MAP)
		
			pygame.display.flip()
	
	
	def start_computer_checkers(self, minimax_depth=None, red_heur="posicional",black_heur="posicional"):
		global DONE, GAME_TEXT
		
		self.__init__(self.screen)
		self.screen = pygame.display.set_mode(self.board_image.get_size(),RESIZABLE,32)
		
		mm = Decisao_Alfa_Beta(minimax_depth,self,red_heur)
		#mm = Decisao_Minimax(minimax_depth,self,red_heur)
		
		done = False
		DONE = False
		while not done and not DONE:
			
			self.screen.fill((0,0,0))
			self.screen.blit(self.board_image,(0,0))
			self.update(self.screen)
			pygame.display.flip()
			
			estado_minimax = Estado(self.red_pieces,self.black_pieces,BOARD_MAP)
			
			if self.RED_TURN:
				mm.heuristica = red_heur
				#print "heuristica vermelhas:",mm.heuristica
				jo,v = mm.comecar(estado_minimax,estado_minimax.vermelhas,estado_minimax.pretas)
				GAME_TEXT.update_text("Pretas Jogam")
			else:
				mm.heuristica = black_heur
				#print "heuristica pretas   :",mm.heuristica
				jo,v = mm.comecar(estado_minimax,estado_minimax.pretas,estado_minimax.vermelhas)
				GAME_TEXT.update_text("Vermelhas Jogam")
			
			#print "\nTAbuleiro"
			#for l in BOARD_MAP:
				#print l
			
			#print "Valor:",v
			#print "Jogada:"
			#print jo.pos_inicial
			#print jo.pos_meio
			#print jo.pos_final
			#print jo.captura
			
			self.play(jo)
			self.RED_TURN = not self.RED_TURN
			
			self.events()
			self.update(self.screen)
			done = self.end_of_game(BOARD_MAP)
			
			pygame.display.flip()
	
	
	#
	def events(self):
		global DONE
		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				pygame.quit()
				sys.exit(-1)
			elif event.type == pygame.MOUSEMOTION:
				self.mouse_motion()
			elif event.type == pygame.MOUSEBUTTONDOWN:
				if event.button == 1:	# left button
					if self.mouse_clicked() >= 0:
						print "AQUI DEVE SAIR"
						DONE = True
					
	
	def mouse_clicked(self):
		m_pos = pygame.mouse.get_pos()
		for b in self.buttons:
			if b.rect.collidepoint(m_pos):
				return b.action
		
		if(self.RED_TURN):
			pieces = self.red_pieces		#  red  turn to select one piece
		else: pieces = self.black_pieces	# black turn to select one piece
		
		if not self.selected_piece and not CAPTURE_MODE:
			self.select_piece(pieces)
		else:
			self.move_piece(pieces)
		
		return -1
	
	
	def mouse_motion(self):
		m_pos = pygame.mouse.get_pos()
		for b in self.buttons:
			if b.rect.collidepoint(m_pos):
				b.set_selected()
			else: b.set_unselected()
	
	#
	def select_piece(self,pieces):
		moves = self.generate_moves(pieces,BOARD_MAP)
		piece = None
		
		for p in pieces:
			if p.rect.collidepoint(pygame.mouse.get_pos()):
				piece = p
		
		if piece:
			for m in moves:
				if piece.position == m[0].position:
					self.selected_piece = piece
					self.selected_piece.set_image_selected()
					break
			if not self.selected_piece:
				print "Peca Invalida"
		else: print "Selecione uma Peca"
	
	#
	def move_piece(self,pieces):
		global CAPTURE_MODE, CAPTURE_LIST, CAPTURE_COUNT
		x_m,y_m = pygame.mouse.get_pos()
		row = y_m/self.TILE_Y
		col = x_m/self.TILE_X
		
		# se a peça de selecionada for clicada, será deselecionada caso esteja em modo de captura
		if  self.selected_piece.rect.collidepoint(pygame.mouse.get_pos()) and not CAPTURE_MODE:
			self.selected_piece.set_image_default()
			self.selected_piece = None
		else:
			# senão irá tentar mover a peça para a nova posição
			if CAPTURE_MODE:
				moves = self.generate_moves([self.selected_piece],BOARD_MAP)
			else:
				moves = self.generate_moves(pieces,BOARD_MAP)
			
			move = []
			for m in moves:
				if m[0].position == self.selected_piece.position:
					move = m
					break
			
			if move:
				x_p, y_p = self.selected_piece.position
				for i in range(len(move[1])):				# para cada movimento possivel
					if (row,col) == move[1][i]:
						BOARD_MAP[x_p][y_p] = '.'
						BOARD_MAP[row][col] = self.selected_piece.group
						self.selected_piece.position = (row,col)
						if len(move[2]) > 0:				# a jogada posssui capturas
							CAPTURE_MODE = True
							BOARD_MAP[move[2][i][0]][move[2][i][1]] = 'x'
							CAPTURE_LIST.append(move[2][i])	# remover a peça capturada
							CAPTURE_COUNT = 0
						else:
							CAPTURE_COUNT += 1
						break
					i += 1
				
				if i >= len(move[1]):
					return
				
				if CAPTURE_MODE:
					has_moves = self.selected_piece.get_moves(BOARD_MAP)
					if len(has_moves[1]) == 0:
						CAPTURE_MODE = False
						for i in CAPTURE_LIST:
							self.remove_piece(i)
						CAPTURE_LIST = []
						if self.selected_piece.position[0] == self.selected_piece.MAX_ROW:
							self.selected_piece.promote()
						self.selected_piece.set_image_default()
						self.selected_piece = None
						self.RED_TURN = not self.RED_TURN
				
				elif not CAPTURE_MODE:
					if self.selected_piece.position[0] == self.selected_piece.MAX_ROW:
						self.selected_piece.promote()
					for i in CAPTURE_LIST:
						self.remove_piece(i.position)
					CAPTURE_LIST = []
					self.selected_piece.set_image_default()
					self.selected_piece = None
					self.RED_TURN = not self.RED_TURN
			
				print "COUNT", CAPTURE_COUNT
			
			else:
				print "Jogada Inválida",self.selected_piece.position
	
	#
	def remove_piece(self, pos):
		if self.RED_TURN:
			pieces = self.black_pieces
		else: pieces = self.red_pieces
		for p in pieces:
			if p.position == pos:
				pieces.remove(p)
				BOARD_MAP[pos[0]][pos[1]] = '.'
				break
	
	#
	def update(self,screen):
		for piece in self.red_pieces:
			x,y = piece.position
			piece.rect = screen.blit(piece.surface,(y*self.TILE_Y,x*self.TILE_X))
		
		for piece in self.black_pieces:
			x,y = piece.position
			piece.rect = screen.blit(piece.surface,(y*self.TILE_Y,x*self.TILE_X))
		
		for i in self.itens:
			i.draw(screen, self.font)
	
	#
	def capture_pieces(self,board,piece):
		"""
			método invocado no modo de captura (CAPTURE_MODE)
			responsável por analisar as capturas em sequência
			possíveis e retornar o movimento (ou sequencia de
			jogadas) que tem maior número de capturas.
		"""
		moves = piece.get_moves(board)
		
		if len(moves[1]) == 0:		# se não tiver capturas seguintes
			return 0,None,None		# retornar 0 para o número de capturas e None para a movimentação seguinte e a captura realizada
		
		count = 0
		next_move = []
		capt_move = []
		for i in range(len(moves[0])): 		# para cada movimento da peça - verificar o número de capturas realizadas
			px,py = piece.position
			board[px][py] = '.'
			b = copy.deepcopy(board)
			p = copy.deepcopy(piece)
			p.position = moves[0][i]
			b[moves[0][i][0]][moves[0][i][1]] = p.group
			b[moves[1][i][0]][moves[1][i][1]] = 'x'
			
			c,nmov,cap = self.capture_pieces(b, p)
			c += 1
			if c > count:
				count = c
				next_move = [moves[0][i]]
				capt_move = [moves[1][i]]
			elif c == count:
				next_move.append(moves[0][i])
				capt_move.append(moves[1][i])
		return count, next_move, capt_move
	
	#
	def generate_moves(self,pieces,board):
		"""
			método  responsável por analisar  e  retornar
			as jogadas possíveis de um conjunto de peças.
		"""
		moves = []
		captures = False
		for p in pieces:
			m = p.get_moves(board)
			if len(m[0]) > 0: 		# SE TIVER JOGADAS
				if len(m[1]) > 0 and not captures: 	# se tiver capturas mas nenhuma captura adicionada
					moves = []						# limpar jogadas
					captures = True					# apenas jogadas com capturas
				if captures:									# se já tem capturas
					if len(m[1]) > 0:							# adicionar apenas jogadas com capturas
						moves.append([p, m[0],m[1]])
				else: moves.append([p, m[0],m[1]])		# se não tiver capturas, adicionar jogada
		
		if captures:
			mc = [[None,[],[]]] # move/capture = [Piece,[(moves)],[(captures)]
			capt_num = 0
			
			for m in moves: # para cada peça com movimentos de captura
				piece = m[0]
				
				c,mov,cap = self.capture_pieces(copy.deepcopy(board), copy.copy(piece))
				
				if c > capt_num:
					capt_num = c
					mc = []
				if c == capt_num:
					mc.append([piece,mov,cap])
			
			return mc
		else:
			return moves
	
	#
	def end_of_game(self,board):
		if self.RED_TURN:
			pieces = self.red_pieces
		else:
			pieces = self.black_pieces
		
		if len(self.generate_moves(pieces,board)) == 0:
			if self.RED_TURN:
				print "FIM DE JOGO, Pretas Venceram"
			else:
				print "FIM DE JOGO, Vermelhas Venceram"
			return True
		
		if CAPTURE_COUNT >= 40:		# 20 jogadas de cada jogador
			print "FIM DE JOGO, EMPATE"
			return True
		
		R,r = 0,0
		B,b = 0,0
		
		if CAPTURE_COUNT >= 10:		# 5 jogadas de cada jogador
			for ps in [self.red_pieces,self.black_pieces]:
				for p in ps:
					if p.group == 'r':
						r += 1
					elif p.group == 'R':
						R += 1
					elif p.group == 'b':
						b += 1
					elif p.group == 'B':
						B += 1
		
			for p,o in [[R,r],[B,b]],[[B,b],[R,r]]:
				if p[0] <= 2 and p[1] == 0:	# 2 ou 1 dama
					if o[0] <= 2 and o[1] == 0:
						print "FIM DE JOGO, Empate"
						return True
					if o[0] == 1 and o[1] <= 1:	# x 1 dama e 1 ou 0 peça
						print "FIM DE JOGO, Empate"
						return True
		
		
		return False
	
	def fim_de_jogo(self,estado):
		if len(estado.vermelhas) == 0 or len(self.generate_moves(estado.vermelhas,estado.tabuleiro)) == 0:
			return True
		elif len(estado.pretas) == 0 or len(self.generate_moves(estado.pretas,estado.tabuleiro)) == 0:
			return True
		
		# CASOS DE EMPATE
		if CAPTURE_COUNT >= 40:		# 20 jogadas de cada jogador
			print "FIM DE JOGO, EMPATE"
			return True
		
		R,r = 0,0
		B,b = 0,0
		
		if CAPTURE_COUNT >= 10:		# 5 jogadas de cada jogador
			for ps in [self.red_pieces,self.black_pieces]:
				for p in ps:
					if p.group == 'r':
						r += 1
					elif p.group == 'R':
						R += 1
					elif p.group == 'b':
						b += 1
					elif p.group == 'B':
						B += 1
		
			for p,o in [[R,r],[B,b]],[[B,b],[R,r]]:
				if p[0] <= 2 and p[1] == 0:	# 2 ou 1 dama
					if o[0] <= 2 and o[1] == 0:
						print "FIM DE JOGO, Empate"
						return True
					if o[0] == 1 and o[1] <= 1:	# x 1 dama e 1 ou 0 peça
						print "FIM DE JOGO, Empate"
						return True
		
		
		return False
		
	
	
	#
	def play(self, movimento):
		global BOARD_MAP, CAPTURE_COUNT
		
		jogador = None
		oponente = None
		peca = None
		
		#print movimento.pos_inicial
		#print movimento.pos_meio
		#print movimento.pos_final
		#print movimento.captura
		#for l in BOARD_MAP:
			#print l
		
		# encontrar a apeça responsável pelo movimento
		p_ini = movimento.pos_inicial
		casa = BOARD_MAP[p_ini[0]][p_ini[1]]
		if casa == 'r' or casa == 'R':
			jogador = self.red_pieces
			oponente = self.black_pieces
		elif casa == 'b' or casa == 'B':
			jogador = self.black_pieces
			oponente = self.red_pieces
		else:
			print "ERRO - A casa a ser movida não representa uma peça"
		
		for p in jogador:
			if p.position == p_ini:
				peca = p
				break
		
		# movimentar a peça
		p_ant = p_ini
		while len(movimento.pos_meio)>0:
			p_mov = movimento.pos_meio[0]
			#print "Captura em sequencia",p_mov
			peca.position = p_mov
			BOARD_MAP[p_mov[0]][p_mov[1]] = peca.group
			#print ">",p_ant
			BOARD_MAP[p_ant[0]][p_ant[1]] = '.'
			movimento.pos_meio.remove(p_mov)
			p_ant = p_mov
			
			self.update(self.screen)
			pygame.display.flip()
		
		p_fin = movimento.pos_final
		peca.position = p_fin
		if peca.position[0] == peca.MAX_ROW:
			peca.promote()
		BOARD_MAP[p_fin[0]][p_fin[1]] = peca.group
		#print "_",p_ant
		BOARD_MAP[p_ant[0]][p_ant[1]] = '.'
		
		if len(movimento.captura) > 0:
			CAPTURE_COUNT = 0
			for p in copy.copy(oponente):
				if p.position in movimento.captura:
					#print "Removeu",p.position
					BOARD_MAP[p.position[0]][p.position[1]] = '.'
					oponente.remove(p)
		else:
			CAPTURE_COUNT += 1
		
		#print "Fim da Jogada"
		#print "Tabuleiro"
		#for l in BOARD_MAP:
			#print l
		#print "Vermelhas"
		#for p in self.red_pieces:
			#print p.position
		#print "Pretas"
		#for p in self.black_pieces:
			#print p.position


class Piece(object):
	def __init__(self,surface,pos,group):
		self.surface = surface
		self.position = pos
		self.group = group
		self.rect = None
	
	#
	def set_image_default(self):
		""" Define the image for a not selected piece """
		self.surface = self.default_image
	
	#
	def set_image_selected(self):
		""" Define the image for a selected piece """
		self.surface = self.selected_image
	
	#
	@abstractmethod
	def front_row(self,row):
		pass
	
	#
	@abstractmethod
	def back_row(self,row):
		pass
	
	#
	@abstractmethod
	def left_col(self, col):
		pass
	#
	@abstractmethod
	def right_col(self, col):
		pass
	
	#
	def is_move(self,row,col):
		if ( row < 8 and row >= 0 and col < 8 and col >= 0 ):
			return True
		else: return False
	
	#
	def get_moves(self,board):
		moves = [[],[]]
		captures = False
		
		row,col = self.position
		
		#	 MOVEMENTO DE PEÇAS SIMPLES 	#
		if self.group == 'r' or self.group == 'b':
			new_row = self.front_row(row)
			new_col = self.left_col(col)
			if self.is_move(new_row,new_col):
				if board[new_row][new_col] == '.' and not captures:
					moves[0].append((new_row,new_col))
				elif board[new_row][new_col] in self.OPPONENT:
					new_row = self.front_row(new_row)
					new_col = self.left_col(new_col)
					if self.is_move(new_row,new_col) and board[new_row][new_col] == '.':
						if not captures:
							moves = [[],[]]
							captures = True
						moves[0].append((new_row,new_col))
						moves[1].append((self.back_row(new_row),self.right_col(new_col)))
			
			new_row = self.front_row(row)
			new_col = self.right_col(col)
			if self.is_move(new_row,new_col):
				if board[new_row][new_col] == '.' and not captures:
					moves[0].append((new_row,new_col))
				elif board[new_row][new_col] in self.OPPONENT:
					new_row = self.front_row(new_row)
					new_col = self.right_col(new_col)
					if self.is_move(new_row,new_col) and board[new_row][new_col] == '.':
						if not captures:
							moves = [[],[]]
							captures = True
						moves[0].append((new_row,new_col))
						moves[1].append((self.back_row(new_row),self.left_col(new_col)))
			
			new_row = self.back_row(row)
			new_col = self.left_col(col)
			if self.is_move(new_row,new_col) and board[new_row][new_col] in self.OPPONENT:
				new_row = self.back_row(new_row)
				new_col = self.left_col(new_col)
				if self.is_move(new_row,new_col) and board[new_row][new_col] == '.':
					if not captures:
						moves = [[],[]]
						captures = True
					moves[0].append((new_row,new_col))
					moves[1].append((self.front_row(new_row),self.right_col(new_col)))
			
			new_row = self.back_row(row)
			new_col = self.right_col(col)
			if self.is_move(new_row,new_col) and board[new_row][new_col] in self.OPPONENT:
				new_row = self.back_row(new_row)
				new_col = self.right_col(new_col)
				if self.is_move(new_row,new_col) and board[new_row][new_col] == '.':
					if not captures:
						moves = [[],[]]
						captures = True
					moves[0].append((new_row,new_col))
					moves[1].append((self.front_row(new_row),self.left_col(new_col)))
		
		#	 FIM MOVIMENTO DAS PEÇAS SIMPLES	#
		
		#	MOVIMENTO DE DAMAS	#
		elif self.group == 'R' or self.group == 'B':
			#	  DAMAS -> FRENTE / ESQUERDA 	# 
			new_row = self.front_row(row)
			new_col = self.left_col(col)
			m = [[],[]]	# possíveis movimentos gerados na diagonal
			eat = None	# armazena a peça capturada na diagonal
			while(self.is_move(new_row,new_col)):
				if board[new_row][new_col] in self.FRIEND:
					break
				elif board[new_row][new_col] == 'x':
					break
				elif board[new_row][new_col] in self.OPPONENT:
					if not eat:
						r = self.front_row(new_row)
						c = self.left_col(new_col)
						if self.is_move(r,c) and board[r][c] == ".":
							captures = True
							eat = (new_row,new_col)
							m = [[],[]]
						else: break
					else: break
				elif board[new_row][new_col] == '.':
					m[0].append((new_row,new_col))
					if eat:
						m[1].append(eat)
				new_row = self.front_row(new_row)
				new_col = self.left_col(new_col)
			
			if len(m[1]) > 0:
				if len(moves[1]) == 0:
					moves = [[],[]]
				for i in m[0]:
					moves[0].append(i)
				for i in m[1]:
					moves[1].append(i)
			elif not captures:
				for i in m[0]:
					moves[0].append(i)
			#	  FIM DAMAS -> FRENTE / ESQUERDA 	# 
			
			#	  DAMAS -> FRENTE / DIREITA 	# 
			new_row = self.front_row(row)
			new_col = self.right_col(col)
			m = [[],[]]	# possíveis movimentos gerados na diagonal
			eat = None	# armazena a peça capturada na diagonal
			while(self.is_move(new_row,new_col)):
				if board[new_row][new_col] in self.FRIEND:
					break
				elif board[new_row][new_col] == 'x':
					break
				elif board[new_row][new_col] in self.OPPONENT:
					if not eat:
						r = self.front_row(new_row)
						c = self.right_col(new_col)
						if self.is_move(r,c) and board[r][c] == ".":
							captures = True
							eat = (new_row,new_col)
							m = [[],[]]
						else: break
					else: break
				elif board[new_row][new_col] == '.':
					m[0].append((new_row,new_col))
					if eat:
						m[1].append(eat)
				new_row = self.front_row(new_row)
				new_col = self.right_col(new_col)
			
			if len(m[1]) > 0:
				if len(moves[1]) == 0:
					moves = [[],[]]
				for i in m[0]:
					moves[0].append(i)
				for i in m[1]:
					moves[1].append(i)
			elif not captures:
				for i in m[0]:
					moves[0].append(i)
			#	FIM DAMAS -> FRENTE / DIREITA	#
			
			#	  DAMAS -> ATRÁS / ESQUERDA 	# 
			new_row = self.back_row(row)
			new_col = self.left_col(col)
			m = [[],[]]	# possíveis movimentos gerados na diagonal
			eat = None	# armazena a peça capturada na diagonal
			while(self.is_move(new_row,new_col)):
				if board[new_row][new_col] in self.FRIEND:
					break
				elif board[new_row][new_col] == 'x':
					break
				elif board[new_row][new_col] in self.OPPONENT:
					if not eat:
						r = self.back_row(new_row)
						c = self.left_col(new_col)
						if self.is_move(r,c) and board[r][c] == ".":
							captures = True
							eat = (new_row,new_col)
							m = [[],[]]
						else: break
					else: break
				elif board[new_row][new_col] == '.':
					m[0].append((new_row,new_col))
					if eat:
						m[1].append(eat)
				new_row = self.back_row(new_row)
				new_col = self.left_col(new_col)
			
			if len(m[1]) > 0:
				if len(moves[1]) == 0:
					moves = [[],[]]
				for i in m[0]:
					moves[0].append(i)
				for i in m[1]:
					moves[1].append(i)
			elif not captures:
				for i in m[0]:
					moves[0].append(i)
			
			#	FIM DAMAS -> ATRÁS / ESQUERDA	#
			
			#	  DAMAS -> ATRÁS / DIREITA 	# 
			new_row = self.back_row(row)
			new_col = self.right_col(col)
			m = [[],[]]	# possíveis movimentos gerados na diagonal
			eat = None	# armazena a peça capturada na diagonal
			while(self.is_move(new_row,new_col)):
				if board[new_row][new_col] in self.FRIEND:
					break
				elif board[new_row][new_col] == 'x':
					break
				elif board[new_row][new_col] in self.OPPONENT:
					if not eat:
						r = self.back_row(new_row)
						c = self.right_col(new_col)
						if self.is_move(r,c) and board[r][c] == ".":
							captures = True
							eat = (new_row,new_col)
							m = [[],[]]
						else: break
					else: break
				elif board[new_row][new_col] == '.':
					m[0].append((new_row,new_col))
					if eat:
						m[1].append(eat)
				new_row = self.back_row(new_row)
				new_col = self.right_col(new_col)
			
			if len(m[1]) > 0:
				if len(moves[1]) == 0:
					moves = [[],[]]
				for i in m[0]:
					moves[0].append(i)
				for i in m[1]:
					moves[1].append(i)
			elif not captures:
				for i in m[0]:
					moves[0].append(i)
			
			#	FIM DAMAS -> ATRÁS / DIREITA	#
			
		#	 FIM MOVIMENTO DE DAMAS 	#
		return moves


class RedPiece(Piece):
	global RED_DEFAULT, RED_DEFAULT_SELECTED
	global RED_CHECKER, RED_CHECKER_SELECTED
	
	OPPONENT = ['b','B']
	FRIEND = ['r','R']
	MIN_COL = 0 # left
	MAX_COL = 7 # right
	MIN_ROW = 7 # back
	MAX_ROW = 0 # forward
	
	def __init__(self,pos):
		Piece.__init__(self,RED_DEFAULT,pos,'r')
		self.default_image  = RED_DEFAULT
		self.selected_image = RED_DEFAULT_SELECTED
	#
	def promote(self):
		self.group = 'R'
		self.surface =        RED_CHECKER
		self.default_image  = RED_CHECKER
		self.selected_image = RED_CHECKER_SELECTED
	#
	def front_row(self,row):
		return row - 1
	#
	def back_row(self, row):
		return row + 1
	#
	def left_col(self,col):
		return col - 1
	#
	def right_col(self,col):
		return col + 1


class BlackPiece(Piece):
	global BLACK_DEFAULT, BLACK_DEFAULT_SELECTED
	global BLACK_CHECKER, BLACK_CHECKER_SELECTED
	
	OPPONENT = ['r','R']
	FRIEND = ['b','B']
	MIN_COL = 7 # left
	MAX_COL = 0 # right
	MIN_ROW = 0 # back
	MAX_ROW = 7 # forward
	
	def __init__(self,pos):
		Piece.__init__(self,BLACK_DEFAULT,pos,'b')
		self.default_image  = BLACK_DEFAULT
		self.selected_image = BLACK_DEFAULT_SELECTED
	
	#
	def promote(self):
		self.group = 'B'
		self.surface =        BLACK_CHECKER
		self.default_image  = BLACK_CHECKER
		self.selected_image = BLACK_CHECKER_SELECTED
	#
	def front_row(self,row):
		return row + 1
	#
	def back_row(self, row):
		return row - 1
	#
	def left_col(self,col):
		return col + 1
	#
	def right_col(self,col):
		return col - 1
	