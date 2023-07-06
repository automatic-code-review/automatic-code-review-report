# automatic-code-review-report

Projeto que sera usado de webhook para os comentarios adicionados, permitindo assim fazer análise de dados

- Revisão manual
  - De início para verificar se os comentarios automaticos estão corretos, existe uma página em específico para "approvar" o comentario, permitindo assim uma revisão manual, visando garantir no início que as verificações estão corretas
- Grafana
  - Gerar graficos e infos referente aos dados coletados
    - Quantidade total de comentarios
    - Quantidade de comentarios por extensao
    - Quantidade de comentarios por usuario
    - Quantidade de comentarios por usuario e por extensao

# Docker
```shell
sudo docker-compose up -d --build
```
