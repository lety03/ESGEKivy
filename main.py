from kivymd.app import MDApp
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.gridlayout import GridLayout
from kivy.uix.scrollview import ScrollView
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput
from kivymd.uix.button import MDRectangleFlatButton
from kivymd.uix.button import MDRoundFlatButton
from kivymd.uix.button import MDIconButton
from kivymd.uix.dialog import MDDialog
from kivymd.uix.button import MDFloatingActionButtonSpeedDial
import sqlite3


manager = ScreenManager()

#tela de login do usuario
class LoginWindow(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.subgrid = GridLayout()
        self.subgrid.size_hint_y = 0.5
        self.add_widget(self.subgrid)
        con = sqlite3.connect('test.db')
        cursor = con.cursor()

        cursor.execute('SELECT usuario FROM Usuarios WHERE manterConectado = 1')
        resultado = cursor.fetchall()

        if resultado != []:
            manager.switch_to(HomeWindow())

        con.commit()
        con.close()
        pass
    def Acessar(self):
        
        nome = self.ids.nome.text
        senha = self.ids.senha.text
        
        if (nome != '' and senha != ''):
            con = sqlite3.connect('test.db')
            cursor = con.cursor()
            cursor.execute('SELECT usuario FROM Usuarios WHERE usuario = ? AND senha = ?;', (nome,senha))

            rows = cursor.fetchall()
            if(rows != []):
                cursor.execute('UPDATE Usuarios SET manterConectado = 1 WHERE usuario = ? ;', (nome,))
                con.commit()
                con.close()

                manager.switch_to(HomeWindow())
                pass
            else:
                self.ids.msg.text = 'Usuário inexistente.'
        else:
            self.ids.msg.text = 'Usuário ou senha inexistente.'
        

class CadastroUsuarioWindow(Screen):
    def __init__(self, **kw):
        super().__init__(**kw)

    def CadastrarUsuario(self):
        nome = self.ids.nome.text
        senha = self.ids.senha.text

        if (nome !='' and senha != ''):
                
                con = sqlite3.connect('test.db')

                cursor = con.cursor()
                try:
                    cursor.execute('SELECT usuario FROM Usuarios WHERE usuario = ?', (nome,))
                    rows = cursor.fetchall()
                except:
                    self.ids.msg.text = 'Error desconhecido, tente novamente.'
                    return 'erro'
                    
                    
                

                if (rows == []):
                    try:
                        cursor.execute('INSERT INTO Usuarios (usuario,senha) VALUES(?,?)', (nome,senha))
                    except:
                        self.ids.msg.text = 'Error cadastrar, tente novamente.'
                        con.commit()
                        con.close()
                        return 'erro'

                    con.commit()
                    con.close()

                    self.ids.msg.text = 'Usuário cadastrado!'
                else:
                    con.commit()
                    con.close()
                    self.ids.msg.text = 'Usuário já existente.'

#tela de cadastro de produto
class CadastroProdutoWindow(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.cols = 1
        self.rows = 8
        self.subgrid = GridLayout()
        self.add_widget(self.subgrid)
        pass

    def CriarItem(self):
        

        nomeItem = self.ids.nomeProduto.text
        qntIdeal = self.ids.quantidadeIdeal.text
        qntAtual = self.ids.quantidadeAtual.text
        
        if nomeItem != '':
            con = sqlite3.connect('test.db')
            cursor = con.cursor()

            cursor.execute('SELECT usuario FROM Usuarios WHERE manterConectado = 1')
            resultadoNome = cursor.fetchall()
            nomeUsuario = resultadoNome[0][0]

            try:
                cursor.execute('SELECT nomeItem FROM Items WHERE nomeItem = ? AND nomeUsuario = ?', (nomeItem,nomeUsuario))
                rows = cursor.fetchall()
            except:
                self.ids.msg.text = 'Error desconhecido, tente novamente.'
                return 'erro'
            
            if rows == []:
                cursor.execute('INSERT INTO Items (nomeItem,quantidadeIdeal,quantidadeAtual,nomeUsuario) VALUES(?,?,?,?)',(nomeItem,qntIdeal,qntAtual,nomeUsuario))
                self.ids.msg.text = 'Item cadastrado com sucesso!'
            else:
                self.ids.msg.text = 'Item já existente!'
            con.commit()
            con.close()

    def DeletarWid(self):
        # manager.current = 'home'
        self.remove_widget(self.children[0])

#tela de alteração dos produtos
class ListaProdutoWindow(Screen, GridLayout):

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.scroll = ScrollView(always_overscroll=True,do_scroll_y=True,bar_color=(.8, .7, .7, .9))
        self.gridLy = BoxLayout(orientation='vertical')
        self.ExibirItems()

    def LimparGrid(self):
        self.scroll.clear_widgets()
        self.gridLy.clear_widgets()

    def ExibirItems(self):

        if len(self.children) >= 4:
            try:
                self.clear_widgets([self.gridLy])
            except:
                print('erro ao excluir grid')
            try:
                self.clear_widgets([self.scroll])
            except:
                print('erro ao excluir scroll')

        self.LimparGrid()
        
        self.grid = GridLayout(size_hint_y=None)
        self.cols = 1
        self.scroll.size_hint = ("0.3dp", 1)

        con = sqlite3.connect('test.db')

        cursor = con.cursor()

        cursor.execute('SELECT usuario FROM Usuarios WHERE manterConectado = 1')
        resultadoNome = cursor.fetchall()

        if resultadoNome != []:
            nome = resultadoNome[0][0]

            cursor.execute('SELECT nomeItem,quantidadeIdeal,quantidadeAtual FROM Items WHERE nomeUsuario = ?', (nome,))

            resultadoItems = cursor.fetchall()

            if resultadoItems != []:
                qntItem = len(resultadoItems)
                self.grid.cols  = 1
                self.grid.rows = qntItem
                
                for x in resultadoItems:
                    
                    btnItem = MDRectangleFlatButton(text='' , on_press=self.ExibirAlterar)

                    btnItem.gridBtn = GridLayout()
                    btnItem.gridBtn.cols = 3
                    btnItem.gridBtn.add_widget(Label(text=x[0],font_size='10sp',padding=(10, 10), size_hint_x=1 ,  text_size=(100, None)))
                    btnItem.gridBtn.add_widget(Label(text=str(x[1]), font_size='10sp',padding=(10, 10), size_hint_x=1))
                    btnItem.gridBtn.add_widget(Label(text=str(x[2]), font_size='10sp',padding=(10, 10), size_hint_x=1))

                    
                    btnItem.size_hint_x = 1
                    btnItem.size_hint_y = None
                    btnItem.size = '100dp','100dp'

                    btnItem.add_widget(btnItem.gridBtn)
                    self.grid.add_widget(btnItem)

                self.grid.bind(minimum_height = self.grid.setter("height"))
                self.scroll.add_widget(self.grid)
                self.scroll.size_hint_y =1
                self.scroll.size_hint_x = 1
                self.scroll.pos = 0,0
                self.scroll.index = 1
                self.scroll.pos = 0,0

                self.add_widget(self.scroll, len(self.children))
            else:
                self.gridLy.add_widget(Label(text='Não há itens cadastrados.'))
                self.add_widget(self.gridLy, len(self.children))
                
        else:
            self.gridLy = BoxLayout(orientation='vertical')
            self.gridLy.add_widget(Label(text='Faça login!'))
            return self.gridLy
    
    def ExibirAlterar(self, instance = [], nomeAlt = '', qntItem = '0', qntIdeal = '0'):
        '''
        ADICIONAR O PARAMETRO ID A FUNÇÃO 
        '''

        # Buscando os valores o item
        if nomeAlt == '' and qntItem == '0' and qntIdeal == '0':
            nomeAlt = instance.gridBtn.children[2].text
            qntItem = instance.gridBtn.children[1].text
            qntIdeal = instance.gridBtn.children[0].text

        # Limpando o layout
        self.clear_widgets()

        # Declarando layout da janela e do form do produto
        self.floatLy = FloatLayout()
        self.gridLy = GridLayout()

        # Ajustando a o grid
        self.gridLy.size_hint = .8, .8
        self.gridLy.cols = 1
        self.gridLy.rows = 8

        # Adicionando a label e inputs do form 
        self.gridLy.add_widget(Label(text='Produto', size_hint_y=0.5))
        lbItem = TextInput(text=nomeAlt)
        lbItem.size_hint_y=None 
        lbItem.size = '50dp','30dp'
        self.gridLy.add_widget(lbItem)
        self.gridLy.add_widget(Label(text='Quantidade Atual' , size_hint_y=0.5))
        lbAtual = TextInput(text=qntItem)
        lbAtual.size_hint_y=None 
        lbAtual.size = '50dp','30dp'
        self.gridLy.add_widget(lbAtual)
        self.gridLy.add_widget(Label(text='Quantidade Ideal', size_hint_y=0.5))
        lbIdeal = TextInput(text=qntIdeal)
        lbIdeal.size_hint_y=None 
        lbIdeal.size = '50dp','30dp'
        self.gridLy.add_widget(lbIdeal)

        # Criando e Adicionando botões de salvar e voltar
        self.dialog = MDDialog(
        title="Excluir Item?",
        text="Isto irá excluir o item permanentemente.",
        buttons=[
            MDRoundFlatButton(
                text="Sim",
                theme_text_color="Custom",
                on_press=lambda x:self.ExcluirItem(nomeAlt),
                on_release=lambda x:self.__init__(),
            ),
            MDRoundFlatButton(
                text="Não",
                theme_text_color="Custom",
                on_press=lambda x:self.ExcluirPopUp('deletar',nomeAlt, str(qntItem), str(qntIdeal)),
            ),
        ],
        )
        self.dialog.pos_hint = {'center_y': .5, 'center_x': .5}
        self.dialog.index = 1
        # btnExcluir = MDIconButton(icon='storefront-minus', on_press=lambda x:self.ExcluirItem(nomeAlt))
        btnExcluir = MDIconButton(icon='storefront-minus', on_press=lambda x:self.dialog.open())
        btnExcluir.theme_text_color= "Error"
        btnExcluir.hint_animation= True
        # btnExcluir.text_color = self.theme_cls.theme_style
        btnExcluir.pos_hint={'center_y': .9, 'center_x': .9}
        btnSalvar = MDRoundFlatButton(text='Salvar',on_press=lambda x:self.AlterarItem(nomeAlt, lbItem.text, lbAtual.text, lbIdeal.text))
        btnHome = MDRoundFlatButton(text='Voltar', on_press=lambda x:self.remove_widget(self.floatLy) , on_release=lambda x:self.__init__())
        btnSalvar.size_hint_x = 0.1
        btnSalvar.pos_hint = {'center_x': 0.5}
        btnHome.size_hint_x = 0.2
        btnHome.pos_hint = {'center_x': 0.5}
        # self.floatLy.add_widget(self.dialog)
        self.floatLy.add_widget(btnExcluir)
        self.gridLy.add_widget(btnSalvar)
        self.gridLy.add_widget(btnHome)
        self.gridLy.pos_hint =  {'center_x': 0.5, 'center_y': 0.5}
        self.gridLy.spacing = '10dp'

        # adicionando o layout do form ao layout da pagina 
        self.floatLy.add_widget(self.gridLy)
        # adicionando o layout da pagina
        self.add_widget(self.floatLy)

    def Excluir(self):
        layouAlterar = self.children[0]
        layoutBtn = layouAlterar.children[0]

    def ExcluirPopUp(self, popUp, nomeAlt = '', qntItem = '0', qntIdeal = '0'):
        if popUp == 'deletar':
            self.dialog.dismiss()
        if popUp == 'alterar':
            self.dialogAlterar.dismiss()

    
    def ExcluirItem(self, nomeItem):
        if nomeItem != '':
            con = sqlite3.connect('test.db')
            cursor = con.cursor()

            cursor.execute('DELETE FROM Items WHERE nomeItem = ? ;',(nomeItem,))

            self.ExcluirPopUp('deletar')
            self.remove_widget(self.floatLy)
            con.commit()
            con.close()

    def AlterarItem(self, nomeAnterior, nomeItem,qntAtual, qntIdeal):
        if nomeItem != '':
            print(nomeAnterior)
            print(nomeItem)
            print(qntAtual)
            print(qntIdeal)
            self.dialogAlterar = MDDialog(
            title="Item alterado!",
            text="Alteração salvas",
            buttons=[
                MDRoundFlatButton(
                    text="OK",
                    theme_text_color="Custom",
                    on_press=lambda x:self.ExcluirPopUp('alterar'),
                ),

            ],
            )
            con = sqlite3.connect('test.db')
            cursor = con.cursor()

            cursor.execute('SELECT usuario FROM Usuarios WHERE manterConectado = 1')
            resultadoNome = cursor.fetchall()
            nomeUsuario = resultadoNome[0][0]
            print(nomeUsuario)

            try:
                cursor.execute('SELECT nomeItem FROM Items WHERE nomeItem = ? AND nomeUsuario = ?', (nomeItem,nomeUsuario))
                rows = cursor.fetchall()
            except:
                self.ids.msg.text = 'Error desconhecido, tente novamente.'
                return 'erro'
            
            if rows == []:
                print('vazio')
                cursor.execute('UPDATE Items SET nomeItem = ?, quantidadeAtual = ?, quantidadeIdeal = ? WHERE nomeItem = ? AND nomeUsuario = ? ;',(nomeItem,qntAtual,qntIdeal,nomeAnterior,nomeUsuario))
                self.dialogAlterar.open()
                # self.ids.msg.text = 'Item cadastrado com sucesso!'
            else:
                cursor.execute('UPDATE Items SET quantidadeIdeal = ?, quantidadeAtual = ? WHERE nomeItem = ? AND nomeUsuario = ? ;',(qntIdeal,qntAtual,nomeItem,nomeUsuario))
                self.dialogAlterar.open()
                # self.ids.msg.text = 'Item cadastrado com sucesso!'
            con.commit()
            con.close()
            
        
#tela de busca de produtos
class BuscarProdutoWindow(Screen, GridLayout):

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        self.scroll = ScrollView(always_overscroll=True,do_scroll_y=True,bar_color=(.8, .7, .7, .9))
        self.scroll.size_hint_y = .75
        self.add_widget(self.scroll, index=2)

    def LimparGrid(self):
        self.scroll.clear_widgets()

    def ExibirProduto(self):
        item = self.ids.itemBusca.text
        # resultado = [["apple", 1, 4], ["banana",2,2], ["cherry",3,4]]
        con = sqlite3.connect('test.db')

        cursor = con.cursor()

        cursor.execute('SELECT usuario FROM Usuarios WHERE manterConectado = 1')
        resultadoNome = cursor.fetchall()

        if resultadoNome != []:
            nome = resultadoNome[0][0]

            cursor.execute('SELECT nomeItem,quantidadeIdeal,quantidadeAtual FROM Items WHERE nomeUsuario = ? AND nomeItem LIKE ?;', (nome, item+'%'))

            resultadoItems = cursor.fetchall()


            if resultadoItems != []:
                print(resultadoItems)
                self.grid = GridLayout(size_hint_y=None)
                self.scroll.size_hint_y = .75
                self.grid.pos_hint = {'center_y': .1}
                
                self.scroll.clear_widgets

                self.grid.cols = 1
                self.grid.rows = len(resultadoItems)
                self.grid.spacing = '2dp'

                for x in resultadoItems:           
                    button = MDRectangleFlatButton(on_press=self.ExibirAlterar)
                    button.gridBtn = GridLayout()
                    button.size_hint_x = 1
                    button.size_hint_y = None
                    button.size = '100dp','100dp'
                    button.gridBtn.cols = 3
                    button.gridBtn.add_widget(Label(text=x[0], font_size='10sp', size_hint_x= 2, padding=(10, 10), text_size=(100, None)))
                    button.gridBtn.add_widget(Label(text=str(x[1])))
                    button.gridBtn.add_widget(Label(text=str(x[2])))
                    button.add_widget(button.gridBtn)

                    self.grid.add_widget(button)

                self.grid.bind(minimum_height = self.grid.setter("height"))
                self.scroll.add_widget(self.grid)
                return self.grid
            else:
                boxLy = BoxLayout(size_hint_y=None, orientation='vertical')
                boxLy.add_widget(Label(text='Sem resultados para'))
                boxLy.add_widget(Label(text=str(item)))
                self.scroll.add_widget(boxLy)
                return boxLy
        
    def ExibirAlterar(self, instance = [], nomeAlt = '', qntItem = '0', qntIdeal = '0'):
        '''
        ADICIONAR O PARAMETRO ID A FUNÇÃO 
        '''

        # Buscando os valores o item
        nomeAlt = instance.gridBtn.children[2].text
        qntItem = instance.gridBtn.children[1].text
        qntIdeal = instance.gridBtn.children[0].text

        # Limpando o layout
        self.clear_widgets()

        # Declarando layout da janela e do form do produto
        self.floatLy = FloatLayout()
        self.gridLy = GridLayout()

        # Ajustando a o grid
        self.gridLy.size_hint = .8, .8
        self.gridLy.cols = 1
        self.gridLy.rows = 8

        # Adicionando a label e inputs do form 
        self.gridLy.add_widget(Label(text='Produto', size_hint_y=0.5))
        lbItem = TextInput(text=nomeAlt)
        lbItem.size_hint_y=None 
        lbItem.size = '50dp','30dp'
        self.gridLy.add_widget(lbItem)
        self.gridLy.add_widget(Label(text='Quantidade' , size_hint_y=0.5))
        lbAtual = TextInput(text=qntItem)
        lbAtual.size_hint_y=None 
        lbAtual.size = '50dp','30dp'
        self.gridLy.add_widget(lbAtual)
        self.gridLy.add_widget(Label(text='Quantidade Ideal', size_hint_y=0.5))
        lbIdeal = TextInput(text=qntIdeal)
        lbIdeal.size_hint_y=None 
        lbIdeal.size = '50dp','30dp'
        self.gridLy.add_widget(lbIdeal)

        # Criando e Adicionando botões de salvar e voltar
        btnSalvar = MDRoundFlatButton(text='Salvar')
        btnHome = MDRoundFlatButton(text='Voltar', on_press=lambda x:self.remove_widget(self.floatLy) , on_release=lambda x:self.__init__())
        btnSalvar.size_hint_x = 0.1
        btnSalvar.pos_hint = {'center_x': 0.5}
        btnHome.size_hint_x = 0.2
        btnHome.pos_hint = {'center_x': 0.5}
        self.gridLy.add_widget(btnSalvar)
        self.gridLy.add_widget(btnHome)
        self.gridLy.pos_hint =  {'center_x': 0.5, 'center_y': 0.5}
        self.gridLy.spacing = '10dp'

        # adicionando o layout do form ao layout da pagina 
        self.floatLy.add_widget(self.gridLy)
        # adicionando o layout da pagina
        self.add_widget(self.floatLy)

class RelatorioItemsWindow(Screen):
    def __init__(self, **kw):
        super().__init__(**kw)

        self.scroll = ScrollView(always_overscroll=True,do_scroll_y=True,bar_color=(.8, .7, .7, .9))
        self.scroll.size_hint_y = .75
        self.LimparGrid()
        self.ExibirItems()
        self.add_widget(self.scroll, index=2)

    def LimparGrid(self):
        self.scroll.clear_widgets()

    def ExibirItems(self):

        # Buscar items
        con = sqlite3.connect('test.db')
        cursor = con.cursor()

        cursor.execute('SELECT usuario FROM Usuarios WHERE manterConectado = 1')
        resultadoNome = cursor.fetchall()        
        # resultado = [["apple", 1, 4], ["banana",2,2], ["cherry",3,4], ["apple", 1, 4], ["banana",2,2], ["cherry",3,4], ["apple", 1, 4], ["banana",2,2], ["cherry",3,4], ["apple", 1, 4], ["banana",2,2], ["cherry",3,4]]

        if resultadoNome != []:
            nome = resultadoNome[0][0]

            cursor.execute('SELECT nomeItem,quantidadeIdeal,quantidadeAtual FROM Items WHERE nomeUsuario = ? AND quantidadeIdeal > quantidadeAtual ', (nome,))

            resultadoItems = cursor.fetchall()

            if resultadoItems != '':
                self.grid = GridLayout(size_hint_y=None)
                self.grid.pos_hint = {'center_y': .1}
                
                self.scroll.clear_widgets

                self.grid.cols = 1
                self.grid.rows = len(resultadoItems)
                self.grid.spacing = '2dp'

                for x in resultadoItems:           
                    button = MDRectangleFlatButton()
                    button.gridBtn = GridLayout()
                    button.size_hint_x = 1
                    button.size_hint_y = None
                    button.size = '100dp','100dp'
                    button.gridBtn.cols = 3
                    button.gridBtn.add_widget(Label(text=x[0], font_size='10sp', size_hint_x= 2, padding=(10, 10), text_size=(100, None)))
                    button.gridBtn.add_widget(Label(text=str(x[1])))
                    button.gridBtn.add_widget(Label(text=str(x[2])))
                    button.add_widget(button.gridBtn)

                    self.grid.add_widget(button)

                self.grid.bind(minimum_height = self.grid.setter("height"))
                self.scroll.add_widget(self.grid)
                return self.grid
            else:
                boxLy = BoxLayout(size_hint_y=None, orientation='vertical')
                boxLy.add_widget(Label(text='Nenhum item em falta.'))
                self.scroll.add_widget(boxLy)
                return boxLy
    #tela da home do app
class HomeWindow(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)        
        pass

    # def AlterarVerItems(self):
    #     # ListaProdutoWindow()
    #     manager.switch_to(ListaProdutoWindow(name='AlterarProduto'))

class mainApp(MDApp):

    con = sqlite3.connect('test.db')

    cursor = con.cursor()

    # cursor.execute(''' DROP TABLE Usuarios''')

    # cursor.execute(''' DROP TABLE Items''')


    # cursor.execute('''CREATE TABLE Usuarios(
    #                idUsuario INTEGER PRIMARY KEY,
    #                usuario text,
    #                senha text,
    #                manterConectado INTEGER)''')
    
    # cursor.execute('''CREATE TABLE Items(
    #                idItem INTEGER PRIMARY KEY,
    #                nomeItem text,
    #                quantidadeIdeal INTEGER,
    #                quantidadeAtual INTEGER,
    #                nomeUsuario text)''')
    con.commit()

    con.close()

    def build(self):
        # Crie a variavél/instanciar do screen manager
        self.theme_cls.theme_style = "Dark"
        self.theme_cls.primary_palette = 'Cyan'
        # manager.add_widget(HomeWindow(name='home'))
        manager.add_widget(LoginWindow(name='login'))
        manager.add_widget(CadastroUsuarioWindow(name='CadastroUsuario'))
        manager.add_widget(HomeWindow(name='home'))
        manager.add_widget(ListaProdutoWindow(name='AlterarProduto'))
        manager.add_widget(CadastroProdutoWindow(name='CadastroProduto'))
        manager.add_widget(BuscarProdutoWindow(name='BuscarProduto'))
        manager.add_widget(RelatorioItemsWindow(name='Relatorio'))

        return manager

if __name__=='__main__':
    mainApp().run()
        