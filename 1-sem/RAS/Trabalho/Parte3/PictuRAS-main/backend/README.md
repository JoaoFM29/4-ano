## Run

```
docker compose up -d
docker compose down
```

## Endpoints

- `GET localhost:3001/tools`: obter todas as ferramentas
- `GET localhost:3001/tools/<tool_id>`: obter a ferramenta *tool_id*
- `POST localhost:3001/tools`: adicionar uma ferramenta
- `PUT localhost:3001/tools/<tool_id>`: atualizar a ferramenta *tool_id*
- `DELETE localhost:3001/tools/<tool_id>`: eliminar a ferramenta *tool_id*
- `GET localhost:3002/images`: obter todas as imagens
- `GET localhost:3002/images/<image_id>`: obter a imagem *image_id*
- `GET localhost:3002/images/info/<image_id>`: obter as informações da imagem *image_id*
- `GET localhost:3002/images/data/<image_id>`: obter os *bytes* da imagem *image_id*
- `GET localhost:3002/images/project/<project_id>`: obter as imagens de um projeto
- `POST localhost:3002/images`: adicionar uma image
- `PUT localhost:3002/images/<image_id>`: atualizar a imagem *image_id*
- `DELETE localhost:3002/images/<image_id>`: eliminar a imagem *image_id*
- `GET localhost:3003/projects`: obter todos os projetos
- `GET localhost:3003/projects/<project_id>`: obter o projeto *project_id*
- `GET localhost:3003/projects/owner/<user_id>`: obter os projetos do utilizador *user_id*
- `GET localhost:3003/projects/images/<project_id>`: obter as imagens do projeto *project_id*
- `GET localhost:3003/projects/images/data/<image_id>`: obter os bytes da imagem *image_id* 
- `POST localhost:3003/projects`: adicionar um projeto
- `POST localhost:3003/projects/images/<project_id>`: adicionar uma imagem ao projeto *project_id*
- `PUT localhost:3003/projects/<project_id>`: atualizar o projeto *project_id*
- `DELETE localhost:3003/projects/<project_id>`: eliminar o projeto *project_id*
- `DELETE localhost:3003/projects/images/<image_id>`: eliminar a image *image_id*
- `GET localhost:3004/plans`: obter todos os planos
- `GET localhost:3004/plans/<plan_id>`: obter o plano *plan_id*
- `POST localhost:3004/plans`: adicionar um plano
- `PUT localhost:3004/plans/<plan_id>`: atualizar o plano *plan_id*
- `DELETE localhost:3004/plans/<plan_id>`: eliminar o plano *plan_id*
- `GET localhost:3005/users`: obter todos os utilizadores
- `GET localhost:3005/users/<username>`: obter o utilizador *username*
- `POST localhost:3005/users`: adicionar um utilizador
- `PUT localhost:3005/users/<username>`: atualizar o utilizador *username*
- `DELETE localhost:3005/users/<username>`: eliminar o utilizador *username*