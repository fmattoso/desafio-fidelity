CREATE TABLE IF NOT EXISTS estado (
    cod_uf   serial,
    uf          character(2),
    cod_fornecedor  int,
    nome            varchar(100),
    PRIMARY KEY (cod_uf)
);

CREATE TABLE IF NOT EXISTS servico (
    cod_servico serial,
    civel           varchar(100),
    criminal        varchar(100),
    PRIMARY KEY (cod_servico)
);

CREATE TABLE IF NOT EXISTS lote (
    cod_lote        serial,
    cod_funcionario int, -- Não há uma tabela funcionário
    cod_lote_prazo  interval,
    data_criacao    date DEFAULT current_date,
    tipo            int,
    prioridade      int,
    PRIMARY KEY (cod_lote)
);

CREATE TABLE IF NOT EXISTS pesquisa (
    cod_pesquisa    serial,
    cod_cliente     int,
    cod_uf          int,
    cod_servico     int,
    tipo            int DEFAULT 0,
    cpf             varchar(20),
    cod_uf_nascimento   int,
    cod_uf_rg           int,
    data_entrada    date,
    data_conclusao  date,
    nome            varchar(100),
    nome_corrigido  varchar(100),
    rg              varchar(20),
    rg_corrigido    varchar(20),
    nascimento      date,
    mae             varchar(100),
    mae_corrigido   varchar(100),
    anexo           varchar(800),
    PRIMARY KEY (cod_pesquisa),
    FOREIGN KEY (cod_uf) REFERENCES estado (cod_uf) ON DELETE CASCADE,
    FOREIGN KEY (cod_servico) REFERENCES servico (cod_servico) ON DELETE CASCADE
);

CREATE TABLE IF NOT EXISTS lote_pesquisa (
    -- cod_lote_pesquisa   serial,
    cod_lote            int,
    cod_pesquisa        int,
    cod_funcionario     int, -- Não há uma tabela funcionario
    -- cod_fornecedor      int, -- Está na tabela estado
    -- ata_entrada        date,
    -- data_conclusao      date,
    --codigo_uf           int, -- Está na tabela pesquisa
    obs                 varchar(800),
    PRIMARY KEY (cod_lote, cod_pesquisa),
    FOREIGN KEY (cod_lote) REFERENCES lote (cod_lote) ON DELETE CASCADE,
    FOREIGN KEY (cod_pesquisa) REFERENCES pesquisa (cod_pesquisa) ON DELETE CASCADE
    -- FOREIGN KEY (codigo_uf) REFERENCES estado (codigo_uf) ON DELETE CASCADE
);

CREATE TABLE IF NOT EXISTS pesquisa_spv (
    cod_pesquisa        int,
    cod_spv             int,
    cod_spv_computador  int,
    cod_spv_tipo        int,
    cod_funcionario     int, -- Não há uma tabela funcionário
    filtro              int,
    website_id          int,
    resultado           varchar(100),
    PRIMARY KEY (cod_pesquisa),
    FOREIGN KEY (cod_pesquisa) REFERENCES pesquisa (cod_pesquisa) ON DELETE CASCADE
);

INSERT INTO estado (cod_uf, uf) VALUES (26, 'SP');

ALTER SEQUENCE servico_cod_servico_seq RESTART WITH 1;
INSERT INTO servico (civel, criminal) VALUES ('Cível', 'Criminal');

INSERT INTO pesquisa (cod_servico, cod_uf, nome) VALUES 
    (1, 26, 'Pessoa Sem Processos'),  
    (1, 26, 'Murilo Vieira Miranda'), 
    (1, 26, 'Billy Douglas Cardoso dos Santos'), 
    (1, 26, 'Érika Letícia Guedes Terto'), 
    (1, 26, 'B.B.C.'), 
    (1, 26, 'E.A.L.C.'), 
    (1, 26, 'Jose Abel Messias de Jesus Teixeira'),
    (1, 26, 'Renan José Silva de Souza');

GRANT SELECT, INSERT, UPDATE, DELETE ON ALL TABLES IN SCHEMA public TO fidelity;
GRANT USAGE ON SCHEMA public TO fidelity;
GRANT USAGE, SELECT ON ALL SEQUENCES IN SCHEMA public TO fidelity;