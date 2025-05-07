# Gestão de Images

## EndPoints

- `GET localhost:3002/images`: obter todas as imagens
- `GET localhost:3002/images/<image_id>`: obter a imagem *image_id*
- `GET localhost:3002/images/info/<image_id>`: obter as informações da imagem *image_id*
- `GET localhost:3002/images/data/<image_id>`: obter os *bytes* da imagem *image_id*
- `GET localhost:3002/images/project/<project_id>`: obter as imagens de um projeto
- `POST localhost:3002/images`: adicionar uma image
- `PUT localhost:3002/images/<image_id>`: atualizar a imagem *image_id*
- `DELETE localhost:3002/images/<image_id>`: eliminar a imagem *image_id*