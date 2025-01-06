from datetime import datetime

from flask_wtf import FlaskForm
from flask_wtf.file import FileAllowed, FileField
from wtforms import (
    DateField,
    IntegerField,
    SelectField,
    StringField,
    SubmitField,
    TextAreaField,
)
from wtforms.validators import DataRequired, Length

from app.forms.choices import (
    set_choices,
    set_choicesClasseEPI,
    set_choicesFornecedor,
    set_ChoicesFuncionario,
    set_choicesGrade,
    set_choicesMarca,
    set_choicesModelo,
    set_EpiCautelaChoices,
)

permited_file = FileAllowed(["pdf"], 'Apenas arquivos ".pdf" são permitidos!')

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
]


class CadastroGrade(FlaskForm):
    grade = StringField("Grade", validators=[DataRequired()])
    descricao = TextAreaField("Descrição (Opcional)", default="Sem descrição")
    submit = SubmitField("Salvar")


class InsertEstoqueForm(FlaskForm):
    """
    ### Formulário de inserção de produto no Estoque
    """

    nome_epi = SelectField(
        label="EPI",
        validators=[DataRequired()],
        choices=[],
    )
    tipo_grade = SelectField(
        label="Grade",
        validators=[DataRequired()],
        choices=[],
    )
    tipo_qtd = SelectField(
        label="Tipo de Quantidade(Peça, Unidade, Par, etc)",
        choices=tipo_choices,
        validators=[DataRequired()],
    )
    qtd_estoque = IntegerField(
        label="Quantidade a ser adicionada", validators=[DataRequired()]
    )
    valor_total = StringField(label="Valor Totalizado", validators=[DataRequired()])
    nota_fiscal = FileField(label="Nota Fiscal", validators=[permited_file])
    cod_notafiscal = StringField(label="Cód. Nota Fiscal")

    justificativa = TextAreaField(
        "Justificativa (Para Estornos)",
        default="...",
        render_kw={"maxlength": "128"},
        validators=[Length(max=128)],
    )

    submit = SubmitField(label="Salvar")

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.nome_epi.choices.extend(set_choices())
        self.tipo_grade.choices.extend(set_choicesGrade())


class CadastroEPIForm(FlaskForm):

    ca = SelectField(
        label="CA",
        choices=[
            ("CA Válido", "CA Válido"),
            ("CA Inválido", "CA Inválido"),
            ("CA Não Informado", "CA Não Informado"),
            ("Não Aplicável", "Não Aplicável"),
        ],
    )
    cod_ca = IntegerField(label="Cod CA", validators=[DataRequired()], default="9999")
    nome_epi = StringField(label="EPI", validators=[DataRequired()])

    tipo_epi = SelectField(
        label="Tipo do EPI",
        validators=[DataRequired()],
        choices=[],
    )
    # tipo_epi = StringField(label="Tipo do EPI", validators=[DataRequired()])

    valor_unitario = StringField(label="Valor Unitário", validators=[DataRequired()])
    qtd_entregar = IntegerField(label="Quantidade a Entregar", default=1)
    vencimento = DateField(label="Vencimento CA", default=datetime(2045, 1, 1, 0, 0, 0))
    periodicidade_item = IntegerField(label="Periodicidade do Item", default=90)

    # fornecedor = StringField(label="Fornecedor")
    # marca = StringField(label="Marca")
    # modelo = StringField(label="Modelo")

    fornecedor = SelectField(
        label="Fornecedor",
        choices=[],
    )
    marca = SelectField(
        label="Marca",
        choices=[],
    )
    modelo = SelectField(
        label="Modelo",
        choices=[],
    )

    descricao = TextAreaField("Descrição (Opcional)", default="Sem Descrição")
    filename = FileField(
        label="Foto do EPI",
        id="imagem",
        validators=[FileAllowed(["jpg", "png", "jpeg"], "Images only!")],
    )
    submit = SubmitField(label="Salvar")

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.fornecedor.choices.extend(set_choicesFornecedor())
        self.marca.choices.extend(set_choicesMarca())
        self.modelo.choices.extend(set_choicesModelo())
        self.tipo_epi.choices.extend(set_choicesClasseEPI())


class CadastroCategorias(FlaskForm):
    classe = StringField("Classificação EPI", validators=[DataRequired()])
    descricao = TextAreaField("Descrição (Opcional)", default="Sem descrição")
    submit = SubmitField("Cadastrar")


class CadastroFornecedores(FlaskForm):
    fornecedor = StringField("Fornecedor", validators=[DataRequired()])
    descricao = TextAreaField("Descrição (Opcional)", default="Sem descrição")
    submit = SubmitField("Cadastrar")


class CadastroMarcas(FlaskForm):
    marca = StringField("Marca", validators=[DataRequired()])
    descricao = TextAreaField("Descrição (Opcional)", default="Sem descrição")
    submit = SubmitField("Cadastrar")


class CadastroModelos(FlaskForm):
    modelo = StringField("Modelo", validators=[DataRequired()])
    descricao = TextAreaField("Descrição (Opcional)", default="Sem descrição")
    submit = SubmitField("Cadastrar")


class Cautela(FlaskForm):
    funcionario = SelectField(
        label="Selecione o Funcionário",
        validators=[DataRequired()],
        choices=[],
    )

    nome_epi = SelectField(
        id="selectNomeEpi",
        label="Selecione a EPI",
        choices=[],
    )

    tipo_grade = SelectField(
        id="selectNomeEpi",
        label="Selecione a Grade",
        choices=[],
    )

    qtd_entregar = IntegerField(label="Quantidade para entregar", default=1)
    submit_cautela = SubmitField(id="submit_cautela", label="Emitir documento")

    def __init__(self, choices_grade: list[tuple[str, str]] = None, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.nome_epi.choices.append(("Selecione", "Selecione"))
        self.nome_epi.choices.extend(set_EpiCautelaChoices())

        self.funcionario.choices.append(("Selecione", "Selecione"))
        self.funcionario.choices.extend(set_ChoicesFuncionario())

        if choices_grade:
            self.tipo_grade.choices.extend(choices_grade)
