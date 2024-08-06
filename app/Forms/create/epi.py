from flask_wtf import FlaskForm
from wtforms import (StringField, SubmitField, SelectField, TextAreaField,
                     DateField, IntegerField)
from flask_wtf.file import FileField, FileAllowed
from wtforms.validators import DataRequired, Length

from app.models.EPI import (GradeEPI, ProdutoEPI)
from app.models.Funcionários import Funcionarios

from app import app

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

def set_ChoicesFuncionario() -> list[tuple[str, str]]:
    
    with app.app_context():
        return [(epi.nome_funcionario, epi.nome_funcionario) for epi in Funcionarios.query.all()]

def set_choices() -> list[tuple[str, str]]:

    with app.app_context():
        return [(epi.nome_epi, epi.nome_epi) for epi in ProdutoEPI.query.all()]

def set_choicesGrade() -> list[tuple[str, str]]:

    with app.app_context():
        return [(epi.grade, epi.grade) for epi in GradeEPI.query.all()]

class CadastroGrade(FlaskForm):
    
    grade = StringField("Grade", validators=[DataRequired()])
    descricao = TextAreaField("Descrição (Opcional)")
    submit = SubmitField("Salvar")

class InsertEstoqueForm(FlaskForm):

    nome_epi = SelectField(label='EPI', choices=set_choices(), validators=[DataRequired()])
    tipo_grade = SelectField(label='Grade', choices=set_choicesGrade(), validators=[DataRequired()])
    tipo_qtd = SelectField(label='Tipo de Quantidade(Ex.: Peça, Unidade, Par, etc)', 
                           choices=tipo_choices, validators=[DataRequired()])
    qtd_estoque = IntegerField( label='Quantidade a ser adicionada', validators=[DataRequired()])
    valor_total = StringField(label='Valor Totalizado', validators=[DataRequired()])
    submit = SubmitField(label='Salvar')

class CadastroEPIForm(FlaskForm):

    ca = StringField(label='CA', validators=[DataRequired()])
    cod_ca = IntegerField(label='Cod CA', validators=[DataRequired()])
    nome_epi = StringField(label='Nome do EPI', validators=[DataRequired()])
    tipo_epi = StringField(label='Tipo do EPI', validators=[DataRequired()])
    valor_unitario = StringField(
        label='Valor Unitário', validators=[DataRequired()])
    qtd_entregar = IntegerField(label='Quantidade a Entregar')
    periodicidade_item = IntegerField(label='Periodicidade do Item')
    vencimento = DateField(label='Vencimento', format='%d-%m-%Y')
    fornecedor = StringField(label='Fornecedor')
    marca = StringField(label='Marca')
    modelo = StringField(label='Modelo')
    imagem = FileField(label='Foto do EPI', id="imagem", validators=[
                       FileAllowed(['jpg', 'png', 'jpeg'], 'Images only!')])
    submit = SubmitField(label='Salvar')

class Cautela(FlaskForm):

    select_funcionario = SelectField(label="Selecione o Funcionário", 
    validators=[DataRequired()], choices=set_ChoicesFuncionario())
    
    nome_epi = SelectField(id="selectNomeEpi", label="Selecione a EPI", 
    choices=set_choices())
    
    tipo_grade = SelectField(id="selectNomeEpi", label="Selecione a Grade", choices=[])
    
    qtd_entregar = IntegerField(
        label="Quantidade para entregar", validators=[Length(min=1)])
    submit_cautela = SubmitField(id="submit_cautela", label="Emitir documento")



