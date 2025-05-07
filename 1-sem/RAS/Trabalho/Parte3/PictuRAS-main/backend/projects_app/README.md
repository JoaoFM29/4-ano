# Gestão de Projetos

## EndPoints

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