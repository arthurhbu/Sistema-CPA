# Algumas pendências

Criar uma variável a ser inserida nos relatórios de discentes graduação e pós-graduação (se for o caso) que gere uma tabela de Matriculados e Respondentes por Centro de Ensino.

```
SELECT 
    c.Centro_de_Ensino,
    SUM(c.Matriculados) AS Total_Matriculados_2024,
    SUM(
        COALESCE((
            SELECT MAX(d.TOTAL_DO_CURSO)
            FROM discentes d
            WHERE d.CODICO_CURSO = c.Codigo_Curso
              AND d.ANO_INSTRUMENTO = 2024
        ), 0)
    ) AS Total_Respondentes
FROM cursos c
WHERE c.Ano_Referencia = 2024
GROUP BY c.Centro_de_Ensino
ORDER BY c.Centro_de_Ensino;

```

Exemplo de Saída.
![](docs/backend-doc/Listagem-Centro%20de%20Ensino%20e%20Matriculados.png)


Criar outra variável que deverá apresentar uma tabela de Matriculados e Respondentes por Curso. Se for possível separar por Centro de Ensino.

Abaixo coloco o SQL de exemplo.

```
SELECT 
    c.Centro_de_Ensino,
    c.Nome_Do_Curso,
    c.Matriculados AS Quantidade_Matriculados_2024,
    COALESCE((
        SELECT MAX(d.TOTAL_DO_CURSO)
        FROM discentes d
        WHERE d.CODICO_CURSO = c.Codigo_Curso
          AND d.ANO_INSTRUMENTO = 2024
    ), 0) AS Quantidade_Respondentes,
    ROUND( (
        COALESCE((
            SELECT MAX(d.TOTAL_DO_CURSO)
            FROM discentes d
            WHERE d.CODICO_CURSO = c.Codigo_Curso
              AND d.ANO_INSTRUMENTO = 2024
        ), 0) * 100.0 / c.Matriculados
    ), 2 ) AS Percentual_Respondentes
FROM cursos c
WHERE c.Ano_Referencia = 2024
ORDER BY c.Centro_de_Ensino, c.Nome_Do_Curso;

```

Exemplo de Saída

![](docs/backend-doc/Listagem-cursos%20e%20Matriculados.png)
