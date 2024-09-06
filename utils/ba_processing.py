import os
import osgeo_utils.gdal_calc
from osgeo import gdal
from utils.db_operations import update_percentage

def process_images(data_dir, output_dir, sign, threshold, id_proses):
    data_nir = os.path.join(data_dir, "B8A.tif")
    data_swir = os.path.join(data_dir, "B12.tif")
    
    index_nbr = os.path.join(output_dir, "index_nbr.tif")
    BA_filename_unfiltered = os.path.join(output_dir, "unfiltered_nbr.tif")
    BA_filename_final = os.path.join(output_dir, "ba_nbr.tif")
    
    parameters = ['', '-A', data_nir, '-B', data_swir, '--outfile='+ index_nbr, '--calc="(A.astype(numpy.float32)-B.astype(numpy.float32))/(A.astype(numpy.float32)+B.astype(numpy.float32))"', '--type=Float32']
    osgeo_utils.gdal_calc.main(parameters)
    update_percentage(id_proses, 50)

    parameters = ['', '-A', index_nbr, '--outfile='+ BA_filename_unfiltered, '--calc="A'+ sign +''+ threshold +'"', '--type=Float32']
    osgeo_utils.gdal_calc.main(parameters)
    
    src_ds = gdal.Open(BA_filename_unfiltered)
    band = src_ds.GetRasterBand(1)
    min_val = band.ComputeStatistics(False)[0]
    max_val = band.ComputeStatistics(False)[1]
    scale_params = [min_val, max_val, 0, 1]
    
    opsi_translate = gdal.TranslateOptions(
        format="GTiff",
        noData=str(0),
        scaleParams=[scale_params],
        creationOptions=["COMPRESS=LZW", "TILED=YES"]
    )
    gdal.Translate(BA_filename_final, BA_filename_unfiltered, options=opsi_translate)
    update_percentage(id_proses, 75)
    
    return BA_filename_final
