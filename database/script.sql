--
-- Script SQL para criação das tabelas de Clientes e Favoritos
--
CREATE TABLE clientes (
    id INT AUTO_INCREMENT PRIMARY KEY,
    nome VARCHAR(255) NOT NULL,
    email VARCHAR(255) NOT NULL UNIQUE, -- Garante que o e-mail não se repita
    senha VARCHAR(255) NOT NULL,      
    data_cadastro TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE favoritos (
    id INT AUTO_INCREMENT PRIMARY KEY,
    cliente_id INT NOT NULL,
    produto_id INT NOT NULL,
    data_favoritado TIMESTAMP DEFAULT CURRENT_TIMESTAMP,

    -- Chave estrangeira com tabela clientes: Se o cliente for deletado, seus favoritos são deletados
    FOREIGN KEY (cliente_id) 
        REFERENCES clientes(id) 
        ON DELETE CASCADE, 
    
    -- Chave composta única: Impede que o mesmo produto seja favoritado duas vezes pelo mesmo cliente
    UNIQUE (cliente_id, produto_id) 
);