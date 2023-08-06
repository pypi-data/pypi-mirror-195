# USAGE
## import library
import easyGIS
## Contries support: 'vietnamese' only now.
eG = easyGIS(country='vie')
## Load data
dataLoader = eG.loadDatabase()
## Give an example location
pts = [21.038575823260388, 105.77209179475015]
result = eG.findout(pts,dataLoader)
## Result
print(ret)
# {'ward': 'Mai Dịch', 'district': 'Cầu Giấy', 'province': 'Hà Nội'}