# Frontend

## Project setup
```
npm install
```

### Compiles and hot-reloads for development
```
npm run dev
```

### Compiles and minifies for production
```
npm run build
```

### Image Compression

```
from PIL import Image
import os
import glob
import re
for f in glob.glob('YOUR_IMAGE_DIR/*'):
    print(f)
    if re.search("png|jpg|jpeg", f.split(".")[1], re.IGNORECASE):
        output_path = os.path.join("./YOUR_IMAGE_DIR", os.path.basename(f).split(".")[0]+".webp")
        print(output_path)
        image = Image.open(f)
        image.save(output_path, "webp")
```
