-- Dump SQL para MySQL
-- Banco de dados: `projeto_rotas`

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
START TRANSACTION;
SET time_zone = "+00:00";

SET NAMES utf8mb4;

-- Criar o banco de dados
CREATE DATABASE IF NOT EXISTS `projeto_rotas` DEFAULT CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci;
USE `projeto_rotas`;

-- Tabela: alojamentos
CREATE TABLE `alojamentos` (
  `id` INT NOT NULL AUTO_INCREMENT,
  `nome` VARCHAR(100) NOT NULL,
  `endereco` VARCHAR(150) NOT NULL,
  `numero` VARCHAR(10) NOT NULL,
  `cidade` VARCHAR(100) NOT NULL,
  `estado` VARCHAR(2) NOT NULL,
  `data_cadastro` DATE NOT NULL DEFAULT CURRENT_DATE,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- Tabela: obras
CREATE TABLE `obras` (
  `id` INT NOT NULL AUTO_INCREMENT,
  `nome` VARCHAR(100) NOT NULL,
  `endereco` VARCHAR(150) NOT NULL,
  `numero` VARCHAR(10) NOT NULL,
  `cidade` VARCHAR(100) NOT NULL,
  `estado` VARCHAR(2) NOT NULL,
  `data_cadastro` DATE NOT NULL DEFAULT CURRENT_DATE,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- Tabela: usuarios
CREATE TABLE `usuarios` (
  `id` INT NOT NULL AUTO_INCREMENT,
  `nome` VARCHAR(100) NOT NULL,
  `email` VARCHAR(100) NOT NULL,
  `senha` VARCHAR(255) NOT NULL,
  `data_cadastro` DATE NOT NULL DEFAULT CURRENT_DATE,
  PRIMARY KEY (`id`),
  UNIQUE (`email`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- Tabela: veiculos
CREATE TABLE `veiculos` (
  `id` INT NOT NULL AUTO_INCREMENT,
  `quantidade_passageiros` INT NOT NULL,
  `modelo` VARCHAR(100) NOT NULL,
  `cor` VARCHAR(50) NOT NULL,
  `placa` VARCHAR(10) NOT NULL,
  `data_cadastro` DATE NOT NULL DEFAULT CURRENT_DATE,
  `obra_id` INT DEFAULT NULL,
  `nome` VARCHAR(100) NOT NULL,
  `endereco` VARCHAR(150) NOT NULL,
  `numero` VARCHAR(10) NOT NULL,
  `cidade` VARCHAR(100) NOT NULL,
  `estado` VARCHAR(2) NOT NULL,
  `latitude` DECIMAL(10,7) DEFAULT NULL,
  `longitude` DECIMAL(10,7) DEFAULT NULL,
  PRIMARY KEY (`id`),
  UNIQUE (`placa`),
  KEY `obra_id` (`obra_id`),
  CONSTRAINT `fk_veiculos_obra` FOREIGN KEY (`obra_id`) REFERENCES `obras` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- Tabela: funcionarios
CREATE TABLE `funcionarios` (
  `id` INT NOT NULL AUTO_INCREMENT,
  `nome_completo` VARCHAR(150) NOT NULL,
  `cpf` VARCHAR(14) NOT NULL,
  `alojamento_id` INT NOT NULL,
  `obra_id` INT DEFAULT NULL,
  `veiculo_id` INT DEFAULT NULL,
  `usuario_id` INT DEFAULT NULL,
  `data_cadastro` DATE NOT NULL DEFAULT CURRENT_DATE,
  PRIMARY KEY (`id`),
  UNIQUE (`cpf`),
  KEY `alojamento_id` (`alojamento_id`),
  KEY `obra_id` (`obra_id`),
  KEY `veiculo_id` (`veiculo_id`),
  KEY `usuario_id` (`usuario_id`),
  CONSTRAINT `fk_funcionarios_alojamento` FOREIGN KEY (`alojamento_id`) REFERENCES `alojamentos` (`id`),
  CONSTRAINT `fk_funcionarios_obra` FOREIGN KEY (`obra_id`) REFERENCES `obras` (`id`),
  CONSTRAINT `fk_funcionarios_veiculo` FOREIGN KEY (`veiculo_id`) REFERENCES `veiculos` (`id`),
  CONSTRAINT `fk_funcionarios_usuario` FOREIGN KEY (`usuario_id`) REFERENCES `usuarios` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

COMMIT;
