from flask_wtf import FlaskForm
from wtforms import (StringField, SubmitField, SelectField, TextAreaField,
                     DateField, IntegerField)
from flask_wtf.file import FileField, FileAllowed
from wtforms.validators import DataRequired, Length

class CadastroGrade(FlaskForm):
    
    grade = StringField("Grade", validators=[DataRequired()])
    descricao = TextAreaField("Descrição (Opcional)")
    submit = SubmitField("Salvar")

class InsertEstoqueForm(FlaskForm):

    nome_epi = SelectField(label='EPI', choices=[("Vazio", "Selecione")], validators=[DataRequired()])
    tipo_grade = SelectField(label='Grade', choices=[("Vazio", "Selecione")], validators=[DataRequired()])
    tipo_qtd = SelectField(label='Tipo de Quantidade(Ex.: Peça, Unidade, Par, etc)', 
                           choices=[("Vazio", "Selecione")], validators=[DataRequired()])
    
    qtd_estoque = IntegerField( label='Quantidade em Estoque', validators=[DataRequired()])
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

    select_funcionario = SelectField(label="Selecione o Funcionário", validators=[
                                     DataRequired()], choices=[("Vazio", "Selecione")])
    nome_epi = SelectField(id="selectNomeEpi", label="Selecione a EPI", choices=[
                           ("Vazio", "Selecione")])
    tipo_grade = SelectField(
        id="selectNomeEpi", label="Selecione a Grade", choices=[])
    qtd_entregar = IntegerField(
        label="Quantidade para entregar", validators=[Length(min=1)])
    submit_cautela = SubmitField(id="submit_cautela", label="Emitir documento")



