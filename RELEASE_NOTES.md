# Release Notes

## v1.0.0 (Initial Release)
- Flask web app for Diabetic Retinopathy detection
- Pretrained models included (`model/inceptionResnetV2.h5`, `model/custom_cnn.h5`)
- Frontend static files served from `static/`
- Simple upload and inference flow
- Dockerfile provided for containerized deployment

Known notes:
- Large model files are tracked via Git LFS. If cloning from GitHub, run `git lfs install && git lfs pull` to fetch them.
- If downloading a source archive (zip/tar) from GitHub without LFS assets, models may be missing; use the release ZIP artifact or `git lfs pull`.