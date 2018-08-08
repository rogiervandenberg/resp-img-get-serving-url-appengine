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
