Serving Responsive Images via Google Cloud Storage and Images Python API
==================================

Google Cloud storage can do a lot of interesting things by itself. If you combine it with [Images Python API](https://developers.google.com/appengine/docs/python/images/), you can use the =sXXX param to get properly scaled images that you can use for various breakpoints via picture or src-set.

### Prerequisites

1. You can either create a new project in the [Google Developers Console](https://console.developers.google.com) and use that or you can integrate the very basic route into an existing project. Up to you.
2. You'll need the [Google Cloud SDK](https://developers.google.com/cloud/sdk/) to be able to use gcloud deploy.

### Setup

1. Clone this repo
```
git clone https://github.com/rogiervandenberg/resp-img-get-serving-url-appengine.git
```
2. Install the requirements so that our project will run (Flask, et cetera)
```
pip install -r requirements.txt -t lib
```
4. Make your own key entry in config.ini
5. Deploy to App Engine: `gcloud app deploy`

### Getting started

Getting a serving url:

```
curl --data "bucket=myawesomebucket&image=rock-bench-knights-ferry.jpg?key=123" SOMETHING.appspot.com/serveurl
curl --data "bucket=myawesomebucket&image=rock-bench-knights-ferry.jpg?key=123" SOMETHING.appspot.com/serveurl
```

Which will return a url that looks something like:

```
https://lh5.ggpht.com/rCGu26RVMiLkEepYZhhfmxMxsKrb29wUFGfqirbErbNvmLqVlr7mFvXILGQrSZ_u53D4OpMSh_wN3lUoh224RhWWFJlFQA
```

### Gotcha's and things

1. Only one app can "own" the image. As stated in the [documentation](https://developers.google.com/appengine/docs/python/images/functions) for get_serving_url:

> If you serve images from Google Cloud Storage, you cannot serve an image from two separate apps. Only the first app that calls get_serving_url on the image can get the URL to serve it because that app has obtained ownership of the image.

2. Can't scale up above 1600 pixels. As a matter of fact, the Image service won't scale an image beyond the uploads intial size (don't expect the service to scale 32px image to 1600px).

3. The serving url is inherently public (no support for private serving urls).

4. It is not possible to remove an image from the Google Cache

5. Probably other things that I'm forgetting at the moment.

### Getting image manipulations with your image
Usage Example
We can effect various image transformations by tacking strings onto the end of an App Engine blob-based image URL, following an = character. Options can be combined by separating them with hyphens, eg.:

`http://[image-url]=s200-fh-p-b10-c0xFFFF0000`

`http://[image-url]=s200-r90-cc-c0xFF00FF00-fSoften=1,20,0:`


#### SIZE / CROP
* s640 — generates image 640 pixels on largest dimension
* s0 — original size image
* w100 — generates image 100 pixels wide
* h100 — generates image 100 pixels tall
* s (without a value) — stretches image to fit dimensions
* c — crops image to provided dimensions
* n — same as c, but crops from the center
* p — smart square crop, attempts cropping to faces
* pp — alternate smart square crop, does not cut off faces (?)
* cc — generates a circularly cropped image
* ci — square crop to smallest of: width, height, or specified =s parameter
* nu — no-upscaling. Disables resizing an image to larger than its original resolution.

#### PAN AND ZOOM
* x, y, z: — pan and zoom a tiled image. These have no effect on an untiled image or without an authorization parameter * of some form (see googleartproject.com).

#### ROTATION
* fv — flip vertically
* fh — flip horizontally
* r{90, 180, 270} — rotates image 90, 180, or 270 degrees clockwise

#### IMAGE FORMAT
* rj — forces the resulting image to be JPG
* rp — forces the resulting image to be PNG
* rw — forces the resulting image to be WebP
* rg — forces the resulting image to be GIF

v{0,1,2,3} — sets image to a different format option (works with JPG and WebP)

Forcing PNG, WebP and GIF outputs can work in combination with circular crops for a transparent background. Forcing JPG can be combined with border color to fill in backgrounds in transparent images.


#### ANIMATED GIFs
* rh — generates an MP4 from the input image
* k — kill animation (generates static image)
* MISC.
* b10 — add a 10px border to image
* c0xAARRGGBB — set border color, eg. =c0xffff0000 for red
* d — adds header to cause browser download
* e7 — set cache-control max-age header on response to 7 days
* l100 — sets JPEG quality to 100% (1-100)
* h — responds with an HTML page containing the image
* g — responds with XML used by Google's pan/zoom

#### Filters
* fSoften=1,100,0: - where 100 can go from 0 to 100 to blur the image
* fVignette=1,100,1.4,0,000000 where 100 controls the size of the gradient and 000000 is RRGGBB of the color of the * border shadow
* fInvert=0,1 inverts the image regardless of the value provided
* fbw=0,1 makes the image black and white regardless of the value provided

Found at: https://stackoverflow.com/questions/25148567/list-of-all-the-app-engine-images-service-get-serving-url-uri-options?answertab=votes#tab-top 
See also https://code-examples.net/en/q/17fbc97 for more missing params