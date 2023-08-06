import numpy as np
import scipy

from digitalarztools.utils.logger import da_logger


class BandProcess:
    def __init__(self, data: np.ndarray):
        self.data = data

    @staticmethod
    def gap_filling(data: np.ndarray, NoDataValue, method=1) -> np.ndarray:
        """
        This function fills the no data gaps in a numpy array

        Keyword arguments:
        dataset -- numpy array
        NoDataValue -- Value that must be filled
        """
        try:
            # fill the no data values
            if NoDataValue is np.nan:
                mask = ~(np.isnan(data))
            else:
                mask = ~(data == NoDataValue)
            xx, yy = np.meshgrid(np.arange(data.shape[1]), np.arange(data.shape[0]))
            xym = np.vstack((np.ravel(xx[mask]), np.ravel(yy[mask]))).T
            data0 = np.ravel(data[:, :][mask])
            data_end = None
            if method == 1:
                interp0 = scipy.interpolate.NearestNDInterpolator(xym, data0)
                data_end = interp0(np.ravel(xx), np.ravel(yy)).reshape(xx.shape)

            if method == 2:
                interp0 = scipy.interpolate.LinearNDInterpolator(xym, data0)
                data_end = interp0(np.ravel(xx), np.ravel(yy)).reshape(xx.shape)

            return data_end
        except Exception as e:
            da_logger.warning(f"Failed in gap filling due to: {str(e)}")
            return data

    @staticmethod
    def create_buffor(Data_In: np.ndarray, Buffer_area=2):
        """
        This function creates a 3D array which is used to apply the moving window
        :param Data_In:
        :param Buffer_area:
        :return:
        """
        # A block of 2 times Buffer_area + 1 will be 1 if there is the pixel in the middle is 1
        Data_Out = np.empty((len(Data_In), len(Data_In[1])))
        Data_Out[:, :] = Data_In
        for ypixel in range(0, Buffer_area + 1):

            for xpixel in range(1, Buffer_area + 1):

                if ypixel == 0:
                    for xpixel in range(1, Buffer_area + 1):
                        Data_Out[:, 0:-xpixel] += Data_In[:, xpixel:]
                        Data_Out[:, xpixel:] += Data_In[:, :-xpixel]

                    for ypixel in range(1, Buffer_area + 1):
                        Data_Out[ypixel:, :] += Data_In[:-ypixel, :]
                        Data_Out[0:-ypixel, :] += Data_In[ypixel:, :]

                else:
                    Data_Out[0:-xpixel, ypixel:] += Data_In[xpixel:, :-ypixel]
                    Data_Out[xpixel:, ypixel:] += Data_In[:-xpixel, :-ypixel]
                    Data_Out[0:-xpixel, 0:-ypixel] += Data_In[xpixel:, ypixel:]
                    Data_Out[xpixel:, 0:-ypixel] += Data_In[:-xpixel, ypixel:]

        Data_Out[Data_Out > 0.1] = 1
        Data_Out[Data_Out <= 0.1] = 0

        return (Data_Out)

    @staticmethod
    def get_summary_data(data: np.ndarray, nodata=None):
        data = data.astype(np.float64)
        data[data == nodata] = np.nan
        mean_val = np.nanmean(data)
        min_val = np.nanmin(data)
        max_val = np.nanmax(data)
        std_val = np.nanstd(data)
        q25_val = np.nanquantile(data, 0.25)
        median_val = np.nanquantile(data, 0.5)
        q75_val = np.nanquantile(data, 0.75)
        return {"mean": mean_val, "median": median_val, "std": std_val,"min": min_val,
                "q25": q25_val, "q75": q75_val, "max": max_val}
