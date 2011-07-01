from PIL.ExifTags import TAGS
import Image
import PIL
import os
import time

BLOG = 'http://masutravel.files.wordpress.com/'

PICTURE_SOURCE = '<a href="%s"><img class="alignnone size-thumbnail" title="%s" src="%s'
PICTURE_SIZE = '?w=%s&#038;h=%s" alt="" width="%s" height="%s" /></a>  '

# datetime of orginial taken picture
# 36867: DateTimeOriginal
DATETIMEORIG = 36867

def _WriteOutput(pictures, fh):
  for item in sorted(pictures):
    fh.write(pictures[item])

def ProcessPath(path):
  date = time.strftime('%Y/%m/')
  directory = os.listdir(path)
  output = open('masu.html', 'w')
  landscape, portrait = {}, {} 
  for filename in directory:
    if filename.lower().endswith('jpg'):
      # We've found a jpg file
      name, _ = os.path.splitext(filename)
      web_name = BLOG + date + filename.lower()
      pic_source = PICTURE_SOURCE % (web_name, name, web_name)
      tmp_img = Image.open(filename)

      # get the exif data
      exif_data = tmp_img._getexif()
      time_taken = time.mktime(
          time.strptime(exif_data[DATETIMEORIG], '%Y:%m:%d %H:%M:%S'))

      # Let's figure out the size
      w, h = tmp_img.size
      if w > h:
        # landscape
        pic_size = PICTURE_SIZE % (150, 100, 150, 100)
        landscape[time_taken] = pic_source + pic_size
      else:
        # portrait
        pic_size = PICTURE_SIZE % (100, 150, 100, 150)
        portrait[time_taken] = pic_source + pic_size

  # Write the landscape stuff
  _WriteOutput(landscape, output)
  output.write('\n\n')
  _WriteOutput(portrait, output)
  output.close()


def main():
  ProcessPath('.')
  
if __name__ == '__main__':
  main()
