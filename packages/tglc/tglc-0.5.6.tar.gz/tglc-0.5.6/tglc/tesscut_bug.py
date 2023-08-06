import astropy.units as u
from astropy.coordinates import SkyCoord
from astroquery.mast import Catalogs
from astroquery.mast import Tesscut

if __name__ == '__main__':
    name = 'TIC 27858644'
    size = 90
    target = Catalogs.query_object(name, radius=21 * 0.707 / 3600, catalog="Gaia", version=2)
    print(f'Target Gaia: {target[0]["designation"]}')
    ra = target[0]['ra']
    dec = target[0]['dec']
    coord = SkyCoord(ra=ra, dec=dec, unit=(u.degree, u.degree), frame='icrs')
    radius = u.Quantity((size + 6) * 21 * 0.707 / 3600, u.deg)
    sector_table = Tesscut.get_sectors(coordinates=coord)
    print(sector_table)
    hdulist = Tesscut.get_cutouts(coordinates=coord, size=size, sector=26)
    print(hdulist[0][1].data['QUALITY'])
