"""
## Formulários para controle de EPI
"""
from app.Forms.choices import (set_ChoicesFuncionario, set_choices, 
                               set_choicesGrade, set_choicesClasseEPI, 
                               set_choicesFornecedor, set_choicesMarca, 
                               set_choicesModelo)

from flask_wtf import FlaskForm
from flask_wtf.form import _Auto
from wtforms import (StringField, SubmitField, SelectField, TextAreaField,
                     DateField, IntegerField)
from flask_wtf.file import FileField, FileAllowed
from wtforms.validators import DataRequired, Length

permited_file = FileAllowed(['pdf'], 'Apenas arquivos ".pdf" são permitidos!')

tipo_choices = [
    ("Peça", "Peça"),
    ("Par", "Par"),
    ("Unidade", "Unidade"),
    ("Dúzia", "Dúzia"),
    ("Centena", "Centena"),
    ("Milhar", "Milhar"),
    ("Litro", "Litro"),
    ("Quilograma", "Quilograma"),
    ("Metro", "Metro"),
    ("Caixa", "Caixa"),
    ("Pacote", "Pacote"),
    ("Galão", "Galão"),
    ("Tonelada", "Tonelada"),
    ("Barril", "Barril"),
    ("Conjunto", "Conjunto"),
    ("Lote", "Lote"),
    ("Fardo", "Fardo"),
    ("Não Especificado", "Não Especificado")
]

class CadastroGrade(FlaskForm):

    grade = StringField("Grade", validators=[DataRequired()])
    descricao = TextAreaField("Descrição (Opcional)")
    submit = SubmitField("Salvar")


class InsertEstoqueForm(FlaskForm):

    """
    ### Formulário de inserção de produto no Estoque
    """

    nome_epi = SelectField(label='EPI', validators=[DataRequired()], choices=[])
    tipo_grade = SelectField(label='Grade', validators=[DataRequired()], choices=[])
    tipo_qtd = SelectField(label='Tipo de Quantidade(Ex.: Peça, Unidade, Par, etc)', choices=tipo_choices, validators=[DataRequired()])
    qtd_estoque = IntegerField(label='Quantidade a ser adicionada', validators=[DataRequired()])
    valor_total = StringField(label='Valor Totalizado',validators=[DataRequired()])
    nota_fiscal = FileField(label="Nota Fiscal", validators=[DataRequired(), permited_file])
    cod_notafiscal = StringField(label="Cód. Nota Fiscal", validators=[DataRequired()])
    
    submit = SubmitField(label='Salvar')

    def __init__(self, *args, **kwargs):

        super(InsertEstoqueForm, self).__init__(*args, **kwargs)
        self.nome_epi.choices.extend(set_choices())
        self.tipo_grade.choices.extend(set_choicesGrade())


class CadastroEPIForm(FlaskForm):

    ca = StringField(label='CA', validators=[DataRequired()])
    cod_ca = IntegerField(label='Cod CA', validators=[DataRequired()])
    nome_epi = StringField(label='EPI', validators=[DataRequired()])
    tipo_epi = SelectField(label='Tipo do EPI', validators=[DataRequired()], choices=[])
    valor_unitario = StringField(
        label='Valor Unitário', validators=[DataRequired()])
    qtd_entregar = IntegerField(label='Quantidade a Entregar')
    periodicidade_item = IntegerField(label='Periodicidade do Item')
    vencimento = DateField(label='Vencimento')
    fornecedor = SelectField(label='Fornecedor', choices=[])
    marca = SelectField(label='Marca', choices=[])
    modelo = SelectField(label='Modelo', choices=[])
    filename = FileField(label='Foto do EPI', id="imagem", validators=[
                       FileAllowed(['jpg', 'png', 'jpeg'], 'Images only!')])
    submit = SubmitField(label='Salvar')

    def __init__(self, *args, **kwargs):

        super(CadastroEPIForm, self).__init__(*args, **kwargs)
        self.fornecedor.choices.extend(set_choicesFornecedor())
        self.marca.choices.extend(set_choicesMarca())
        self.modelo.choices.extend(set_choicesModelo())
        self.tipo_epi.choices.extend(set_choicesClasseEPI())

class CadastroClasses(FlaskForm):

    classe = StringField("Classificação EPI", validators=[DataRequired()])
    descricao = TextAreaField("Descrição (Opcional)")
    submit = SubmitField("Cadastrar")
    
class CadastroFonecedores(FlaskForm):

    fornecedor = StringField("Fornecedor", validators=[DataRequired()])
    descricao = TextAreaField("Descrição (Opcional)")
    submit = SubmitField("Cadastrar")
    
class CadastroMarcas(FlaskForm):

    marca = StringField("Marca", validators=[DataRequired()])
    descricao = TextAreaField("Descrição (Opcional)")
    submit = SubmitField("Cadastrar")
    
class CadastroModelos(FlaskForm):

    modelo = StringField("Modelo", validators=[DataRequired()])
    descricao = TextAreaField("Descrição (Opcional)")
    submit = SubmitField("Cadastrar")
    

class Cautela(FlaskForm):

    select_funcionario = SelectField(label="Selecione o Funcionário",
                                     validators=[DataRequired()], choices=[])

    nome_epi = SelectField(id="selectNomeEpi", label="Selecione a EPI",
                           choices=[])

    tipo_grade = SelectField(
        id="selectNomeEpi", label="Selecione a Grade", choices=[])

    qtd_entregar = IntegerField(
        label="Quantidade para entregar", validators=[Length(min=1)])
    submit_cautela = SubmitField(id="submit_cautela", label="Emitir documento")

    def __init__(self, *args, **kwargs):
        super(Cautela, self).__init__(*args, **kwargs)

        self.nome_epi.choices.append(("Selecione", "Selecione"))
        self.nome_epi.choices.extend(set_choices())

        self.select_funcionario.choices.append(("Selecione", "Selecione"))
        self.select_funcionario.choices.extend(set_ChoicesFuncionario())
