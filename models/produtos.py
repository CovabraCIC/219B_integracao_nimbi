from sqlalchemy import (DateTime, Numeric, String, Text, text)
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import declarative_base, mapped_column
from sqlalchemy.dialects.postgresql import DOUBLE_PRECISION


Base = declarative_base()

class DeltaProdutos(Base):
    __tablename__ = 'delta_produtos'
    __table_args__ = {'schema': 'nimbi'}

    codigoitem = mapped_column(String, primary_key=True)
    hash_atual = mapped_column(Text)
    descricao_curta = mapped_column(String)
    descricaolonga = mapped_column(String)
    precoultimacompra = mapped_column(Numeric(10, 2))
    tipo = mapped_column(String)
    marca = mapped_column(String)
    modelo = mapped_column(String)
    sku = mapped_column(String)
    gtin13 = mapped_column(String)
    ncm = mapped_column(String)
    nome_da_unidade_medida = mapped_column(String)
    codigo_do_fabricante = mapped_column(String)
    natureza_de_operacao = mapped_column(String)
    status = mapped_column(String)
    categoria_codigo_da_categoria = mapped_column(String)
    nome_da_imagem = mapped_column(String)
    codigo_do_grupo_de_compras = mapped_column(String)
    
    def __init__(self, **kwargs):
        for key, value in kwargs.items():
            setattr(self, key, value)

class ProdutosNimbi(Base):
    __tablename__ = 'produtos_nimbi'
    __table_args__ = {'schema': 'nimbi'}

    codigoitem = mapped_column(String, primary_key=True)
    descricao_curta = mapped_column(String)
    descricaolonga = mapped_column(String)
    precoultimacompra = mapped_column(DOUBLE_PRECISION)
    tipo = mapped_column(String)
    marca = mapped_column(String)
    modelo = mapped_column(String)
    sku = mapped_column(String)
    gtin13 = mapped_column(String)
    ncm = mapped_column(String)
    nome_da_unidade_medida = mapped_column(String)
    codigo_do_fabricante = mapped_column(String)
    natureza_de_operacao = mapped_column(String)
    status = mapped_column(String)
    categoria_codigo_da_categoria = mapped_column(String)
    nome_da_imagem = mapped_column(String)
    codigo_do_grupo_de_compras = mapped_column(String)
    hash_atual = mapped_column(Text)

    def __init__(self, **kwargs):
        for key, value in kwargs.items():
            setattr(self, key, value)

class SnapshotProdutos(Base):
    __tablename__ = 'snapshot_produtos'
    __table_args__ = {'schema': 'nimbi'}

    codigoitem = mapped_column(String, primary_key=True)
    hash_dados = mapped_column(Text)
    descricao_curta = mapped_column(String)
    descricaolonga = mapped_column(String)
    precoultimacompra = mapped_column(Numeric(10, 2))
    tipo = mapped_column(String)
    marca = mapped_column(String)
    modelo = mapped_column(String)
    sku = mapped_column(String)
    gtin13 = mapped_column(String)
    ncm = mapped_column(String)
    nome_da_unidade_medida = mapped_column(String)
    codigo_do_fabricante = mapped_column(String)
    natureza_de_operacao = mapped_column(String)
    status = mapped_column(String)
    categoria_codigo_da_categoria = mapped_column(String)
    nome_da_imagem = mapped_column(String)
    codigo_do_grupo_de_compras = mapped_column(String)
    data_atualizacao = mapped_column(DateTime, server_default=text('now()'))

    def __init__(self, **kwargs):
        for key, value in kwargs.items():
            setattr(self, key, value)