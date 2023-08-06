# Examples

---

## Information about yourself

```py
import itkdb
client = itkdb.Client()
client.user.authenticate() # (1)!
user = client.get("getUser", json={"userIdentity": client.user.identity})
print([institution["code"] for institution in user["institutions"]])
# ['UCSC', ...]
```

1. If you have not made any requests to the database using the `client` in the
   current session, you need to manually call [itkdb.core.User.authenticate][]
   to instantiate details about the user.

## Information about another user

```py
import itkdb
client = itkdb.Client()
user = client.get("getUser", json={"userIdentity": "23-2145-1"})
print([institution["code"] for institution in user["institutions"]])
# ['UCSC', 'IHEP', 'UBC', 'UCSC_STRIP_SENSORS']
```

## Getting a component

```py
import itkdb
client = itkdb.Client()
component = client.get("getComponent", json={"component":"20USBSX0000421"}) # (1)!
print(f"code={component['code']}, sn={component['serialNumber']}")
# code=0b7346e49f2c2d6153fb940e20da4978, sn=20USBSX0000421
```

1. You can also get a component by it's mongo
   [ObjectId](https://www.mongodb.com/docs/manual/reference/method/ObjectId/),
   or alternative identifier.

## Retrieving a list of components

This example shows how to iterate through components, requesting 32 components
from the database at a time:

```py
import itkdb

client = itkdb.Client()

data = {"project": "P", "pageInfo": {"pageSize": 32}} # (1)!
components_pixels = client.get("listComponents", json=data) # (2)!

print(components_pixels.total) # (3)!

for component in components_pixels: # (4)!
    print(component["code"])
```

1. Each page retrieved from the database will have at most 32 components.
   Strictly speaking, every page but the last page will be guaranteed to have 32
   components.
2. For any request from the database that retrieves a list of items, such as
   `listComponents` or `listInstitutions`, the response typically is paginated
   (wrapped in a `"pageItemList"` key). The [itkdb.Client][] returns a
   [itkdb.responses.PagedResponse][] object that helps deal with the pagination
   by automatically retrieving more pages for you as needed. This line only
   loads the first page (a single HTTP request is made).
3. There's a lot of metadata stored on the [itkdb.responses.PagedResponse][]
   object that is useful for inspection without having to make additional
   requests.
4. [itkdb.responses.PagedResponse][] can be treated like an iterable in python
   and you can just simply iterate over it. As you iterate and exhaust items on
   the currently fetched page, it will automatically make another HTTP request
   to fetch the next page for you (if there is one), or stop the iteration once
   you've reached the limit of items.

## Download an attachment from ITkPD

Downloading an attachment from the database is relatively straightforward. When
using [itkdb.Client][] (and not [itkdb.core.Session][]), the response will
automatically be converted to a [itkdb.models.BinaryFile][]-like object. All
`BinaryFile` have the same baseline set of functionality, with additional
helpers specific to the type of attachment (or file) that has been downloaded
(such as [itkdb.models.ImageFile][] or [itkdb.models.TextFile][]).

In order to reduce the memory overhead, these attachments are ephemeral
(temporarily saved to disk). If you need to persist longer, you can use the
corresponding `attachment.save()` function (see
[itkdb.models.file.BinaryFile.save][]).

=== "Image"

    ```py
    import itkdb
    client = itkdb.Client()

    data = {"code": "bc2eccc58366655352582970d3f81bf46f15a48cf0cb98d74e21463f1dc4dcb9"}

    attachment = client.get("uu-app-binarystore/getBinaryData", json=data) # (1)!
    attachment # <itkdb.models.file.ImageFile(....) file-like object at TMP_PATH> (2)
    attachment.mimetype # 'image/x-canon-cr2' (3)
    attachment.content_type # 'image/x-canon-cr2' (4)
    attachment.extension # 'cr2' (5)
    attachment.filename # 'TMP_PATH' (6)
    attachment.suggested_filename # 'PB6.CR2' (7)
    attachment.size # 35819362 (8)
    attachment.size_fmt # '34.2MiB' (9)

    attachment.save() # saves to disk (10)
    ```

    1. This is an [itkdb.models.ImageFile][].
    2. The attachment object
    3. The mimetype of the content from the response headers
    4. The mimetype of the content using [itkdb.utils.get_mimetype][]
    5. The extension of the file
    6. The filename of the ephemeral file on disk
    7. The filename extracted from the response headers (may not have one!)
    8. The size of the file in bytes
    9. The human-readable size of the file
    10. If no path is specified, will use `suggested_filename` and save to current working directory.

=== "Text"

    ```py
    import itkdb
    client = itkdb.Client()

    data = {"code": "5fd40be3b9f9ada57fa47fe4d8b3c48b26055d5d1c6306d76eb2181d20089879"}

    attachment = client.get("uu-app-binarystore/getBinaryData", json=data) # (1)!
    attachment # <itkdb.models.file.TextFile(....) file-like object at TMP_PATH> (2)
    attachment.mimetype # 'text/plain; charset=UTF-8' (3)
    attachment.content_type # 'text/plain' (4)
    attachment.extension # 'txt' (5)
    attachment.filename # 'TMP_PATH' (6)
    attachment.suggested_filename # 'for_gui test3.txt' (7)
    attachment.size # 23 (8)
    attachment.size_fmt # '23.0B' (9)

    attachment.save() # saves to disk (10)
    ```

    1. This is an [itkdb.models.TextFile][].
    2. The attachment object
    3. The mimetype of the content from the response headers
    4. The mimetype of the content using [itkdb.utils.get_mimetype][]
    5. The extension of the file
    6. The filename of the ephemeral file on disk
    7. The filename extracted from the response headers (may not have one!)
    8. The size of the file in bytes
    9. The human-readable size of the file
    10. If no path is specified, will use `suggested_filename` and save to current working directory.

=== "Zip"

    ```py
    import itkdb
    client = itkdb.Client()

    data = {"code": "143b2c7182137ff619968f4cc41a18ca"}

    attachment = client.get("uu-app-binarystore/getBinaryData", json=data) # (1)!
    attachment # <itkdb.models.file.ZipFile(....) file-like object at TMP_PATH> (2)
    attachment.mimetype # 'application/zip' (3)
    attachment.content_type # 'application/zip' (4)
    attachment.extension # 'zip' (5)
    attachment.filename # 'TMP_PATH' (6)
    attachment.suggested_filename # 'configuration_MODULETHERMALCYCLING.zip' (7)
    attachment.size # 226988 (8)
    attachment.size_fmt # '221.7KiB' (9)

    attachment.save() # saves to disk (10)
    ```

    1. This is an [itkdb.models.ZipFile][].
    2. The attachment object
    3. The mimetype of the content from the response headers
    4. The mimetype of the content using [itkdb.utils.get_mimetype][]
    5. The extension of the file
    6. The filename of the ephemeral file on disk
    7. The filename extracted from the response headers (may not have one!)
    8. The size of the file in bytes
    9. The human-readable size of the file
    10. If no path is specified, will use `suggested_filename` and save to current working directory.

## Upload an attachment

!!! note

    This example uploads an attachment for **components** (`createComponentAttachment`), but you can also do this with **shipments** (`createShipmentAttachment`) and **tests** (`createTestRunAttachment`).

Uploading an attachment to ITkPD or EOS is the same as if you were doing it to
any other API. You can see the documentation from `requests` on how to
[`POST` a multipart-encoded file](https://requests.readthedocs.io/en/latest/user/quickstart/#post-a-multipart-encoded-file).

I recommend that you upload using contexts to automatically close the open file
pointer when done.

=== "ITkPD"

    ```py
    import itkdb
    client = itkdb.Client()

    filename = itkdb.data / "1x1.jpg" # (1)!

    data = {
        "component": "20USE000000086",
        "title": "a test image attachment",
        "description": "a small image shipped with itkdb",
        "url": filename,
        "type": "file"
    }

    with filename.open("rb") as fpointer:
      files = {"data": itkdb.utils.get_file_components({"data": fpointer})} # (2)!
      response = client.post("createComponentAttachment", data=data, files=files) # (3)!

    response['id'] # '63ff7e7d4069b50036fe0ab9'
    response['code'] # '756d0ce0213b856b83da494958d2aab4'
    response['awid'] # 'dcb3f6d1f130482581ba1e7bbe34413c'
    ```

    1. Here, we'll use a small test image that is shipped with `itkdb` for
       demonstration. Feel free to use the same to test your code.
    2. This is typically a tuple specifying the filename, an open pointer to the
       file (readable for streaming the upload), the mimetype, and additional
       headers to set on the request for that specific file. This is specific to how
       `requests` accepts or recognizes the `files` argument here, so refer to their
       documentation. Additionally, [itkdb.utils.get_file_components][] is a
       utility I provide to make this easier to generate (see
       [below](#generating-file-components-for-multipart-uploads) for example
       usage).
    3. While it is called `files` indicating you could upload multiple files, the
       production database only allows uploading a single file.


    The following response keys exist:

    ```py
    ['awid', 'code', 'contentType', 'description', 'filename', 'id', 'name', 'sys', 'tagList', 'versionName']
    ```

=== "EOS"

    ```py
    import itkdb
    client = itkdb.Client(use_eos=True)

    filename = itkdb.data / "1x1.jpg" # (1)!

    data = {
        "component": "20USE000000086",
        "title": "a test image attachment",
        "description": "a small image shipped with itkdb",
        "url": filename,
        "type": "file"
    }

    with filename.open("rb") as fpointer:
      files = {"data": itkdb.utils.get_file_components({"data": fpointer})} # (2)!
      response = client.post("createComponentAttachment", data=data, files=files) # (3)!
      # Ignoring user-specified data={'url': ..., 'type': 'file'} (4)

    response['code'] # '1c0ee8c12a2f7bd43c3ee997b70ab20c'
    response['url'] # 'https://eosatlas.cern.ch/eos/atlas/test/itkpd/1/c/0/1c0ee8c12a2f7bd43c3ee997b70ab20c' (5)
    response['token'] # 'zteos64:...' (6)
    ```

    1. Here, we'll use a small test image that is shipped with `itkdb` for
       demonstration. Feel free to use the same to test your code.
    2. This is typically a tuple specifying the filename, an open pointer to the
       file (readable for streaming the upload), the mimetype, and additional
       headers to set on the request for that specific file. This is specific to how
       `requests` accepts or recognizes the `files` argument here, so refer to their
       documentation. Additionally, [itkdb.utils.get_file_components][] is a
       utility I provide to make this easier to generate (see
       [below](#generating-file-components-for-multipart-uploads) for example
       usage).
    3. This will make two requests, one to the ITkPD API to generate the attachment metadata in the database, and then another request to EOS using the generated metadata from the first request. Additionally, like with ITkPD, EOS only allows uploading a single file.
    4. You will typically see a warning about key/value pairs supplied in the `data` argument that are not being used in the subsequent request to EOS. This is ok, and an indication that the file is in the process of being uploaded to EOS.
    5. The URL on EOS that the file was uploaded to. Notice that it is under three subdirectories named based on the first three characters of the corresponding item mongo [ObjectId](https://www.mongodb.com/docs/manual/reference/method/ObjectId/) for the component, shipment, or test run.
    6.  The ephemeral (short-lived) token associated with the request to upload the file to EOS. Do not save this token as it expires quickly.

    The following response keys exist:

    ```py
    ['code', 'contentType', 'dateTime', 'description', 'filename', 'filesize', 'title', 'token', 'type', 'url', 'userIdentity']
    ```

## Generating file components for multipart uploads

`requests` has a `files` argument that accepts a couple of different sets of
inputs:

```py
{"data": filepointer}
{"data": (filename, filepointer)}
{"data": (filename, filepointer, filetype)}
{"data": (filename, filepointer, filetype, fileheaders)}
```

But [itkdb.utils.get_file_components][] is a utility function to make it easier
to generate this consistently for you. To use, you can run like so:

```py
import itkdb

with (itkdb.data / "1x1.jpg").open("rb") as image_fp,
     (itkdb.data / "1x1.sh").open("rb") as text_fp,
     (itkdb.data / "tiny.root").open("rb") as root_fp:
  itkdb.utils.get_file_components({"data": image_fp})
  # ('1x1.jpg', <_io.BufferedReader...>, 'image/jpeg', {})

  itkdb.utils.get_file_components({"data": ("my-script.sh", text_fp)})
  # ('my-script.sh', <_io.BufferedReader...>, 'text/x-shellscript', {}) (1)

  itkdb.utils.get_file_components({"data": ("analysis.root", root_fp, "application/x+cern-root")})
  # ('analysis.root', <_io.BufferedReader...>, 'application/x+cern-root', {}) (2)
```

1. The filename is `my-script.sh` rather than `1x1.sh`.
2. There is no official mimetype for ROOT files assigned with
   [IANA](https://www.iana.org/assignments/media-types/media-types.xhtml). If
   you don't set one, the default `application/octet-stream` will be used. This
   default is technically ok as the mimetypes are treated as hints/suggestions,
   rather than as a rule.
