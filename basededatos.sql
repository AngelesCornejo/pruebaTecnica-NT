/*SECCION 1.1*/
CREATE DATABASE prueba_tecnica;
USE prueba_tecnica;

SELECT * FROM data_prueba_tecnica;

/*SECCION 1.3*/
CREATE TABLE data_transformed (
    id VARCHAR(40) NOT NULL,
    company_name VARCHAR(130) NOT NULL,
	company_id VARCHAR(40) NOT NULL,
    amount DECIMAL(16,2) NOT NULL,
    status_ VARCHAR(30) NOT NULL,
    created_at TIMESTAMP NOT NULL,
    updated_at TIMESTAMP NULL
);


select * from data_transformed;
/*SECCION 1.4*/
CREATE TABLE companies (
    company_id VARCHAR(40) NOT NULL,
    company_name VARCHAR(130) NOT NULL
);

ALTER TABLE companies ADD PRIMARY KEY (company_id);

INSERT INTO companies (company_id, company_name)
SELECT DISTINCT company_id, company_name
FROM data_transformed
WHERE company_id IS NOT NULL AND company_name IS NOT NULL;

SELECT * FROM companies;

/*Tabla de transacciones (clave primaria: id, FK a companies)*/
CREATE TABLE charges (
	id_charge VARCHAR(40) NOT NULL,
    fkcompany VARCHAR(40) NOT NULL,
    amount DECIMAL(16,2) NOT NULL,
    status_ VARCHAR(30) NOT NULL,
    created_at TIMESTAMP NOT NULL,
    updated_at TIMESTAMP NULL,
    FOREIGN KEY (fkcompany) REFERENCES companies(company_id)
);

INSERT INTO charges (id_charge, fkcompany, amount, status_, created_at, updated_at)
SELECT id, company_id, amount, status_, created_at, updated_at
FROM data_transformed
WHERE company_id IS NOT NULL;

select * from charges;


/*SECCION 1.5*/
/*Consulta y agrupación por ID sin incluir nombres de las compañias*/
SELECT  DATE(created_at) AS fecha, SUM(amount) AS total_transaccionado, fkcompany
FROM charges 
GROUP BY fkcompany, DATE(created_at)
ORDER BY fecha ASC;

CREATE VIEW vista_monto_diario_por_compania AS
SELECT c.company_name AS company_name, DATE(ch.created_at) AS fecha, SUM(ch.amount) AS total_transaccionado
FROM charges ch
JOIN companies c ON ch.fkcompany = c.company_id
GROUP BY c.company_name, DATE(ch.created_at)
ORDER BY fecha ASC, company_name ASC;

SELECT * FROM vista_monto_diario_por_compania;
