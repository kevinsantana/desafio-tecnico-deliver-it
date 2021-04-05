SET TIME ZONE 'America/Sao_Paulo';

-- -----------------------------------------------------
-- DROP TABLES
-- -----------------------------------------------------
DROP TABLE IF EXISTS public."conta";
DROP TABLE IF EXISTS public."dominio_juros";


-- -----------------------------------------------------
-- Table "DOMINIO_JUROS"
-- -----------------------------------------------------
CREATE TABLE public."dominio_juros" (
  "id_juros" SERIAL NOT NULL,
  "dias_em_atraso" SMALLINT NOT NULL UNIQUE,
  "porcentagem_multa" INT NOT NULL,
  "juros_por_dia" FLOAT NOT NULL,
  PRIMARY KEY ("id_juros"));


-- -----------------------------------------------------
-- Table "CONTA"
-- -----------------------------------------------------
CREATE TABLE "conta" (
  "id_conta" SERIAL NOT NULL,
  "nome" VARCHAR(150) NOT NULL,
  "valor_original" FLOAT NOT NULL,
  "data_vencimento" DATE NOT NULL,
  "data_pagamento" DATE NOT NULL,
  PRIMARY KEY ("id_conta"));


-- -----------------------------------------------------
-- INSERT DOMINIO_JUROS
-- -----------------------------------------------------
INSERT INTO public."dominio_juros" ("dias_em_atraso", "porcentagem_multa", "juros_por_dia")
VALUES 
    (3, 2, 0.1),
    (4, 3, 0.2),
    (6, 5, 0.3);