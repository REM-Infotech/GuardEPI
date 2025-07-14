from datetime import datetime

from flask_wtf import FlaskForm
from flask_wtf.file import FileAllowed, FileField
from wtforms import (
    BooleanField,
    DateField,
    IntegerField,
    SelectField,
    StringField,
    SubmitField,
    TextAreaField,
)
from wtforms.validators import DataRequired, Length, StopValidation

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


class BooleanRequired:
    """
    Validates that input was provided for this field.

    Note there is a distinction between this and DataRequired in that
    InputRequired looks that form-input data was provided, and DataRequired
    looks at the post-coercion data. This means that this validator only checks
    whether non-empty data was sent, not whether non-empty data was coerced
    from that data. Initially populated data is not considered sent.

    Sets the `required` attribute on widgets.
    """

    def __init__(self, message=None):
        self.message = message
        self.field_flags = {"required": True}

    def __call__(self, form, field):
        if field.raw_data and field.raw_data[0]:
            return

        if self.message is None:
            message = field.gettext("This field is required.")
        else:
            message = self.message

        field.errors[:] = []
        raise StopValidation(message)


class FormEnvioCautelaAssinada(FlaskForm):
    nome_funcionario = StringField(
        "Funcionário",
        id="nome_funcionario",
        validators=[DataRequired()],
        render_kw={
            "disabled": True,
            "placeholder": "Nome do Funcionário",
        },
    )
    nome_cautela = StringField(
        "Nome Cautela (Arquivo original)",
        id="nome_cautela",
        validators=[DataRequired()],
        render_kw={
            "disabled": True,
            "placeholder": "Nome da Cautela (PDF)",
        },
    )
    arquivo_assinado = FileField(
        "Arquivo assinado",
        id="arquivo_assinado",
        validators=[DataRequired(), permited_file],
    )

    confirm_form = BooleanField(
        "Confirmo que o arquivo enviado refere-se ao arquivo assinado (Ação irreversível!).",
        render_kw={"required": True},
    )

    submit = SubmitField("Enviar")


class CancelarCautelaForm(FlaskForm):
    nome_funcionario = StringField(
        "Funcionário",
        id="nome_funcionario",
        render_kw={
            "disabled": True,
            "placeholder": "Nome do Funcionário",
        },
    )
    nome_cautela = StringField(
        "Nome Cautela (Arquivo original)",
        id="nome_cautela",
        render_kw={
            "disabled": True,
            "placeholder": "Nome da Cautela (PDF)",
        },
    )
    confirm_form = BooleanField(
        "Confirmo que a cautela selecionada refere-se a que desejo cancelar (Ação irreversível!).",
        render_kw={"required": True},
    )

    submit = SubmitField("Solicitar Cancelamento")


class FormGrade(FlaskForm):
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

    def extend_selectors(self):
        self.nome_epi.choices.extend(set_choices())
        self.tipo_grade.choices.extend(set_choicesGrade())


class FormProduto(FlaskForm):
    ca = SelectField(
        label="CA",
        choices=[
            ("CA Válido", "CA Válido"),
            ("CA Inválido", "CA Inválido"),
            ("CA Não Informado", "CA Não Informado"),
            ("Não Aplicável", "Não Aplicável"),
        ],
    )
    cod_ca = IntegerField(label="Cod CA", default=9999)
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

        if not kwargs.get("cod_ca"):
            self.cod_ca.data = 9999

        self.fornecedor.choices.extend(set_choicesFornecedor())
        self.marca.choices.extend(set_choicesMarca())
        self.modelo.choices.extend(set_choicesModelo())
        self.tipo_epi.choices.extend(set_choicesClasseEPI())


class FormCategorias(FlaskForm):
    classe = StringField("Classificação EPI", validators=[DataRequired()])
    descricao = TextAreaField("Descrição (Opcional)", default="Sem descrição")
    submit = SubmitField("Cadastrar")


class FornecedoresForm(FlaskForm):
    fornecedor = StringField("Fornecedor", validators=[DataRequired()])
    descricao = TextAreaField("Descrição (Opcional)", default="Sem descrição")
    submit = SubmitField("Cadastrar")


class FormMarcas(FlaskForm):
    marca = StringField("Marca", validators=[DataRequired()])
    descricao = TextAreaField("Descrição (Opcional)", default="Sem descrição")
    submit = SubmitField("Cadastrar")


class FormModelos(FlaskForm):
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

        self.nome_epi.choices.append(("", "Selecione"))
        self.nome_epi.choices.extend(set_EpiCautelaChoices())

        self.funcionario.choices.append(("", "Selecione"))
        self.funcionario.choices.extend(set_ChoicesFuncionario())

        if choices_grade:
            self.tipo_grade.choices.extend(choices_grade)
