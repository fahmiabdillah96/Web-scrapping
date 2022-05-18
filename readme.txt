I deployed this scrapping data code to download the data from the website of Jakarta health department.
Since to access the data of a region and hospital need to click one by one, we need to make the procedure automatically.

Here is the code we must to change according to the region or time we want to access
- line 22, we have to adjust the index:
  1 = Jakarta Pusat
  2 = Jakarta Utara
  3 = Jakarta Barat
  4 = Jakarta Selatan
  5 = Jakarta Timur
  6 = Kepulauan Seribu
- line 35, adjust the month index
  0 = Januari
  1 = Februari
  11 = Desember
- line 37, adjust the year

After the adjustment, so we will get the data of RS in any region, month, and year. We will get the file data from every hospital so the "final data" is the last file we get.
