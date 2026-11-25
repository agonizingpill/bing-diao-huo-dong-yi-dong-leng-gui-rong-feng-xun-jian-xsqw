from domain.cold_cells_api import router as cold_cells
from domain.thaw_samples_api import router as thaw_samples
from domain.seam_maps_api import router as seam_maps
from domain.cell_swaps_api import router as cell_swaps

routers = (cold_cells, thaw_samples, seam_maps, cell_swaps,)
