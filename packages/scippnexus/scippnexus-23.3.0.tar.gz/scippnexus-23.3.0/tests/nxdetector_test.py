import h5py
import numpy as np
import pytest
import scipp as sc

import scippnexus as snx
from scippnexus import (
    NexusStructureError,
    NXdetector,
    NXentry,
    NXevent_data,
    NXobject,
    NXoff_geometry,
    NXroot,
)


@pytest.fixture()
def nxroot(request):
    """Yield NXroot containing a single NXentry named 'entry'"""
    with h5py.File('dummy.nxs', mode='w', driver="core", backing_store=False) as f:
        root = NXroot(f)
        root.create_class('entry', NXentry)
        yield root


def test_warns_if_no_data_found(nxroot):
    detector_numbers = sc.array(dims=[''], unit=None, values=np.array([1, 2, 3, 4]))
    detector = nxroot.create_class('detector0', NXdetector)
    detector.create_field('detector_numbers', detector_numbers)
    with pytest.warns(UserWarning, match="Failed to load "):
        dg = detector[...]
    assert isinstance(dg, sc.DataGroup)


def test_can_load_fields_if_no_data_found(nxroot):
    detector_numbers = sc.array(dims=[''], unit=None, values=np.array([1, 2, 3, 4]))
    detector = nxroot.create_class('detector0', NXdetector)
    detector.create_field('detector_numbers', detector_numbers)
    detector['detector_numbers'][...]


def test_finds_data_from_group_attr(nxroot):
    da = sc.DataArray(
        sc.array(dims=['xx', 'yy'], unit='K', values=[[1.1, 2.2], [3.3, 4.4]]))
    da.coords['detector_numbers'] = detector_numbers_xx_yy_1234()
    detector = nxroot.create_class('detector0', NXdetector)
    detector.create_field('detector_numbers', da.coords['detector_numbers'])
    detector.create_field('custom', da.data)
    detector.attrs['signal'] = 'custom'
    assert sc.identical(detector[...], da.rename_dims({'xx': 'dim_0', 'yy': 'dim_1'}))


def test_loads_events_when_data_and_events_found(nxroot):
    detector_number = sc.array(dims=[''], unit=None, values=np.array([1, 2]))
    data = sc.ones(dims=['xx'], shape=[2])
    detector = nxroot.create_class('detector0', NXdetector)
    detector.create_field('detector_number', detector_number)
    detector.create_field('data', data)
    assert detector[...].bins is None
    detector.create_field('event_id', sc.array(dims=[''], unit=None, values=[1]))
    detector.create_field('event_time_offset', sc.array(dims=[''], unit='s',
                                                        values=[1]))
    detector.create_field('event_time_zero', sc.array(dims=[''], unit='s', values=[1]))
    detector.create_field('event_index', sc.array(dims=[''], unit='None', values=[0]))
    loaded = detector[...]
    assert loaded.bins is not None
    assert loaded.values[0].variances is None


def detector_numbers_xx_yy_1234():
    return sc.array(dims=['xx', 'yy'], unit=None, values=np.array([[1, 2], [3, 4]]))


def test_loads_data_without_coords(nxroot):
    da = sc.DataArray(sc.array(dims=['xx', 'yy'], values=[[1.1, 2.2], [3.3, 4.4]]))
    da.coords['detector_numbers'] = detector_numbers_xx_yy_1234()
    detector = nxroot.create_class('detector0', NXdetector)
    detector.create_field('detector_numbers', da.coords['detector_numbers'])
    detector.create_field('data', da.data)
    assert sc.identical(detector[...], da.rename_dims({'xx': 'dim_0', 'yy': 'dim_1'}))


@pytest.mark.parametrize('detector_number_key',
                         ['detector_number', 'pixel_id', 'spectrum_index'])
def test_detector_number_key_alias(nxroot, detector_number_key):
    da = sc.DataArray(sc.array(dims=['xx', 'yy'], values=[[1.1, 2.2], [3.3, 4.4]]))
    da.coords[detector_number_key] = detector_numbers_xx_yy_1234()
    detector = nxroot.create_class('detector0', NXdetector)
    detector.create_field(detector_number_key, da.coords[detector_number_key])
    detector.create_field('data', da.data)
    assert sc.identical(detector[...], da.rename_dims({'xx': 'dim_0', 'yy': 'dim_1'}))


def test_select_events_raises_if_detector_contains_data(nxroot):
    da = sc.DataArray(sc.array(dims=['xx', 'yy'], values=[[1.1, 2.2], [3.3, 4.4]]))
    da.coords['detector_numbers'] = detector_numbers_xx_yy_1234()
    detector = nxroot.create_class('detector0', NXdetector)
    detector.create_field('detector_numbers', da.coords['detector_numbers'])
    detector.create_field('data', da.data)
    with pytest.raises(NexusStructureError):
        detector.select_events


def test_loads_data_with_coords(nxroot):
    da = sc.DataArray(
        sc.array(dims=['xx', 'yy'], unit='K', values=[[1.1, 2.2], [3.3, 4.4]]))
    da.coords['detector_numbers'] = detector_numbers_xx_yy_1234()
    da.coords['xx'] = sc.array(dims=['xx'], unit='m', values=[0.1, 0.2])
    detector = nxroot.create_class('detector0', NXdetector)
    detector.create_field('detector_numbers', da.coords['detector_numbers'])
    detector.create_field('xx', da.coords['xx'])
    detector.create_field('data', da.data)
    detector.attrs['axes'] = ['xx', '.']
    assert sc.identical(detector[...], da.rename_dims({'yy': 'dim_1'}))


def test_slicing_works_as_in_scipp(nxroot):
    da = sc.DataArray(
        sc.array(dims=['xx', 'yy'], unit='K', values=[[1.1, 2.2, 3.3], [3.3, 4.4,
                                                                        5.5]]))
    da.coords['detector_numbers'] = sc.array(dims=['xx', 'yy'],
                                             unit=None,
                                             values=np.array([[1, 2, 3], [4, 5, 6]]))
    da.coords['xx'] = sc.array(dims=['xx'], unit='m', values=[0.1, 0.2])
    da.coords['xx2'] = sc.array(dims=['xx'], unit='m', values=[0.3, 0.4])
    da.coords['yy'] = sc.array(dims=['yy'], unit='m', values=[0.1, 0.2, 0.3])
    da.coords['2d_edges'] = sc.array(dims=['yy', 'xx'],
                                     unit='m',
                                     values=[[1, 2, 3], [4, 5, 6], [7, 8, 9]])
    detector = nxroot.create_class('detector0', NXdetector)
    detector.create_field('detector_numbers', da.coords['detector_numbers'])
    detector.create_field('xx', da.coords['xx'])
    detector.create_field('xx2', da.coords['xx2'])
    detector.create_field('yy', da.coords['yy'])
    detector.create_field('2d_edges', da.coords['2d_edges'])
    detector.create_field('data', da.data)
    detector.attrs['axes'] = ['xx', 'yy']
    detector.attrs['2d_edges_indices'] = [1, 0]
    assert sc.identical(detector[...], da)
    assert sc.identical(detector['xx', 0], da['xx', 0])
    assert sc.identical(detector['xx', 1], da['xx', 1])
    assert sc.identical(detector['xx', 0:1], da['xx', 0:1])
    assert sc.identical(detector['yy', 0], da['yy', 0])
    assert sc.identical(detector['yy', 1], da['yy', 1])
    assert sc.identical(detector['yy', 0:1], da['yy', 0:1])
    assert sc.identical(detector['yy', 1:1], da['yy', 1:1])  # empty slice


def create_event_data_ids_1234(group):
    group.create_field('event_id',
                       sc.array(dims=[''], unit=None, values=[1, 2, 4, 1, 2, 2]))
    group.create_field('event_time_offset',
                       sc.array(dims=[''], unit='s', values=[456, 7, 3, 345, 632, 23]))
    group.create_field('event_time_zero',
                       sc.array(dims=[''], unit='s', values=[1, 2, 3, 4]))
    group.create_field('event_index',
                       sc.array(dims=[''], unit='None', values=[0, 3, 3, 5]))


def test_loads_event_data_mapped_to_detector_numbers_based_on_their_event_id(nxroot):
    detector_numbers = sc.array(dims=[''], unit=None, values=np.array([1, 2, 3, 4]))
    detector = nxroot.create_class('detector0', NXdetector)
    detector.create_field('detector_number', detector_numbers)
    create_event_data_ids_1234(detector.create_class('events', NXevent_data))
    assert detector.dims == ('detector_number', )
    assert detector.shape == (4, )
    loaded = detector[...]
    assert sc.identical(
        loaded.bins.size().data,
        sc.array(dims=['detector_number'],
                 unit=None,
                 dtype='int64',
                 values=[2, 3, 0, 1]))
    assert 'event_time_offset' in loaded.bins.coords
    assert 'event_time_zero' in loaded.bins.coords


def test_loads_event_data_with_0d_detector_numbers(nxroot):
    detector = nxroot.create_class('detector0', NXdetector)
    detector.create_field('detector_number', sc.index(1, dtype='int64'))
    create_event_data_ids_1234(detector.create_class('events', NXevent_data))
    assert detector.dims == ()
    assert detector.shape == ()
    loaded = detector[...]
    assert sc.identical(loaded.bins.size().data, sc.index(2, dtype='int64'))


def test_loads_event_data_with_2d_detector_numbers(nxroot):
    detector = nxroot.create_class('detector0', NXdetector)
    detector.create_field('detector_number', detector_numbers_xx_yy_1234())
    create_event_data_ids_1234(detector.create_class('events', NXevent_data))
    assert detector.dims == ('dim_0', 'dim_1')
    assert detector.shape == (2, 2)
    loaded = detector[...]
    assert sc.identical(
        loaded.bins.size().data,
        sc.array(dims=['dim_0', 'dim_1'],
                 unit=None,
                 dtype='int64',
                 values=[[2, 3], [0, 1]]))


def test_select_events_slices_underlying_event_data(nxroot):
    detector = nxroot.create_class('detector0', NXdetector)
    detector.create_field('detector_number', detector_numbers_xx_yy_1234())
    create_event_data_ids_1234(detector.create_class('events', NXevent_data))
    assert sc.identical(
        detector.select_events['pulse', :2][...].bins.size().data,
        sc.array(dims=['dim_0', 'dim_1'],
                 unit=None,
                 dtype='int64',
                 values=[[1, 1], [0, 1]]))
    assert sc.identical(
        detector.select_events['pulse', :3][...].bins.size().data,
        sc.array(dims=['dim_0', 'dim_1'],
                 unit=None,
                 dtype='int64',
                 values=[[2, 2], [0, 1]]))
    assert sc.identical(
        detector.select_events['pulse', 3][...].bins.size().data,
        sc.array(dims=['dim_0', 'dim_1'],
                 unit=None,
                 dtype='int64',
                 values=[[0, 1], [0, 0]]))
    assert sc.identical(
        detector.select_events[...][...].bins.size().data,
        sc.array(dims=['dim_0', 'dim_1'],
                 unit=None,
                 dtype='int64',
                 values=[[2, 3], [0, 1]]))


def test_select_events_slice_does_not_affect_original_detector(nxroot):
    detector = nxroot.create_class('detector0', NXdetector)
    detector.create_field('detector_number', detector_numbers_xx_yy_1234())
    create_event_data_ids_1234(detector.create_class('events', NXevent_data))
    detector.select_events['pulse', 0][...]
    assert sc.identical(
        detector[...].bins.size().data,
        sc.array(dims=['dim_0', 'dim_1'],
                 unit=None,
                 dtype='int64',
                 values=[[2, 3], [0, 1]]))


def test_loading_event_data_creates_automatic_detector_numbers_if_not_present_in_file(
        nxroot):
    detector = nxroot.create_class('detector0', NXdetector)
    create_event_data_ids_1234(detector.create_class('events', NXevent_data))
    assert detector.dims == ['detector_number']
    with pytest.raises(NexusStructureError):
        detector.shape
    loaded = detector[...]
    assert sc.identical(
        loaded.bins.size().data,
        sc.array(dims=['detector_number'],
                 unit=None,
                 dtype='int64',
                 values=[2, 3, 0, 1]))


def test_loading_event_data_with_selection_and_automatic_detector_numbers_raises(
        nxroot):
    detector = nxroot.create_class('detector0', NXdetector)
    create_event_data_ids_1234(detector.create_class('events', NXevent_data))
    assert detector.dims == ['detector_number']
    with pytest.raises(sc.DimensionError):
        detector['detector_number', 0]


def test_loading_event_data_with_full_selection_and_automatic_detector_numbers_works(
        nxroot):
    detector = nxroot.create_class('detector0', NXdetector)
    create_event_data_ids_1234(detector.create_class('events', NXevent_data))
    assert detector.dims == ['detector_number']
    assert tuple(detector[...].shape) == (4, )
    assert tuple(detector[()].shape) == (4, )


def test_event_data_field_dims_labels(nxroot):
    detector_numbers = sc.array(dims=[''], unit=None, values=np.array([1, 2, 3, 4]))
    detector = nxroot.create_class('detector0', NXdetector)
    detector.create_field('detector_number', detector_numbers)
    create_event_data_ids_1234(detector.create_class('events', NXevent_data))
    assert detector['detector_number'].dims == ('detector_number', )


def test_nxevent_data_selection_yields_correct_pulses(nxroot):
    detector = nxroot.create_class('detector0', NXdetector)
    create_event_data_ids_1234(detector.create_class('events', NXevent_data))

    class Load:

        def __getitem__(self, select=...):
            da = detector['events'][select]
            return da.bins.size().values

    assert np.array_equal(Load()[...], [3, 0, 2, 1])
    assert np.array_equal(Load()['pulse', 0], 3)
    assert np.array_equal(Load()['pulse', 1], 0)
    assert np.array_equal(Load()['pulse', 3], 1)
    assert np.array_equal(Load()['pulse', -1], 1)
    assert np.array_equal(Load()['pulse', -2], 2)
    assert np.array_equal(Load()['pulse', 0:0], [])
    assert np.array_equal(Load()['pulse', 1:1], [])
    assert np.array_equal(Load()['pulse', 1:-3], [])
    assert np.array_equal(Load()['pulse', 3:3], [])
    assert np.array_equal(Load()['pulse', -1:-1], [])
    assert np.array_equal(Load()['pulse', 0:1], [3])
    assert np.array_equal(Load()['pulse', 0:-3], [3])
    assert np.array_equal(Load()['pulse', -1:], [1])
    assert np.array_equal(Load()['pulse', -2:-1], [2])
    assert np.array_equal(Load()['pulse', -2:], [2, 1])
    assert np.array_equal(Load()['pulse', :-2], [3, 0])


def create_off_geometry_detector_numbers_1234(group: NXobject,
                                              name: str,
                                              detector_faces: bool = True):
    off = group.create_class(name, NXoff_geometry)
    # square with point in center
    values = np.array([[0, 0, 0], [0, 1, 0], [1, 0, 0], [1, 1, 0], [0.5, 0.5, 0]])
    off['vertices'] = sc.array(dims=['_', 'comp'], values=values, unit='m')
    # triangles
    off['winding_order'] = sc.array(dims=['_'],
                                    values=[0, 1, 4, 1, 2, 4, 2, 3, 4, 3, 0, 4],
                                    unit=None)
    off['faces'] = sc.array(dims=['_'], values=[0, 3, 6, 9], unit=None)
    if detector_faces:
        off['detector_faces'] = sc.array(dims=['_', 'dummy'],
                                         values=[[0, 1], [1, 2], [2, 3], [3, 4]],
                                         unit=None)


@pytest.mark.parametrize('detid_name',
                         ['detector_number', 'pixel_id', 'spectrum_index'])
def test_loads_data_with_coords_and_off_geometry(nxroot, detid_name):
    da = sc.DataArray(
        sc.array(dims=['xx', 'yy'], unit='K', values=[[1.1, 2.2], [3.3, 4.4]]))
    da.coords['detector_number'] = detector_numbers_xx_yy_1234()
    da.coords['xx'] = sc.array(dims=['xx'], unit='m', values=[0.1, 0.2])
    detector = nxroot.create_class('detector0', NXdetector)
    detector.create_field(detid_name, da.coords['detector_number'])
    detector.create_field('xx', da.coords['xx'])
    detector.create_field('data', da.data)
    detector.attrs['axes'] = ['xx', 'yy']
    create_off_geometry_detector_numbers_1234(detector, name='shape')
    loaded = detector[...]
    expected = snx.nxoff_geometry.off_to_shape(
        **detector['shape'][()], detector_number=da.coords['detector_number'])
    assert sc.identical(loaded.coords['shape'].bins.size(),
                        sc.array(dims=da.dims, values=[[1, 1], [1, 1]], unit=None))
    assert sc.identical(loaded.coords['shape'], expected)


def test_missing_detector_numbers_triggers_fallback_given_off_geometry_with_det_faces(
        nxroot):
    var = sc.array(dims=['xx', 'yy'], unit='K', values=[[1.1, 2.2], [3.3, 4.4]])
    detector = nxroot.create_class('detector0', NXdetector)
    detector.create_field('data', var)
    detector.attrs['axes'] = ['xx', 'yy']
    create_off_geometry_detector_numbers_1234(detector, name='shape')
    loaded = detector[...]
    assert isinstance(loaded, sc.DataGroup)
    assert sc.identical(loaded['shape'], detector['shape'][()])


def test_off_geometry_without_detector_faces_loaded_as_0d_with_multiple_faces(nxroot):
    var = sc.array(dims=['xx', 'yy'], unit='K', values=[[1.1, 2.2], [3.3, 4.4]])
    detector = nxroot.create_class('detector0', NXdetector)
    detector.create_field('data', var)
    detector.attrs['axes'] = ['xx', 'yy']
    create_off_geometry_detector_numbers_1234(detector,
                                              name='shape',
                                              detector_faces=False)
    loaded = detector[...]
    assert loaded.coords['shape'].dims == ()
    assert sc.identical(loaded.coords['shape'].bins.size(), sc.index(4))


def create_cylindrical_geometry_detector_numbers_1234(group: snx.NXobject,
                                                      name: str,
                                                      detector_numbers: bool = True):
    shape = group.create_class(name, snx.NXcylindrical_geometry)
    values = np.array([[0, 0, 0], [0, 1, 0], [3, 0, 0]])
    shape['vertices'] = sc.array(dims=['_', 'comp'], values=values, unit='m')
    shape['cylinders'] = sc.array(dims=['_', 'vertex'],
                                  values=[[0, 1, 2], [2, 1, 0]],
                                  unit=None)
    if detector_numbers:
        shape['detector_number'] = sc.array(dims=['_'], values=[0, 1, 1, 0], unit=None)


def test_cylindrical_geometry_without_detector_numbers_loaded_as_0d(nxroot):
    var = sc.array(dims=['xx', 'yy'], unit='K', values=[[1.1, 2.2], [3.3, 4.4]])
    detector = nxroot.create_class('detector0', NXdetector)
    detector.create_field('data', var)
    detector.attrs['axes'] = ['xx', 'yy']
    create_cylindrical_geometry_detector_numbers_1234(detector,
                                                      name='shape',
                                                      detector_numbers=False)
    loaded = detector[...]
    shape = loaded.coords['shape']
    assert shape.dims == ()
    assert sc.identical(shape.bins.size(), sc.index(2))
    assert sc.identical(
        shape.value,
        sc.Dataset({
            'face1_center':
            sc.vectors(dims=['cylinder'], values=[[0, 0, 0], [3, 0, 0]], unit='m'),
            'face1_edge':
            sc.vectors(dims=['cylinder'], values=[[0, 1, 0], [0, 1, 0]], unit='m'),
            'face2_center':
            sc.vectors(dims=['cylinder'], values=[[3, 0, 0], [0, 0, 0]], unit='m'),
        }))


def test_cylindrical_geometry_with_missing_parent_detector_numbers_triggers_fallback(
        nxroot):
    var = sc.array(dims=['xx', 'yy'], unit='K', values=[[1.1, 2.2], [3.3, 4.4]])
    detector = nxroot.create_class('detector0', NXdetector)
    detector.create_field('data', var)
    detector.attrs['axes'] = ['xx', 'yy']
    create_cylindrical_geometry_detector_numbers_1234(detector,
                                                      name='shape',
                                                      detector_numbers=True)
    loaded = detector[...]
    assert isinstance(loaded, sc.DataGroup)
    assert isinstance(loaded['shape'], sc.DataGroup)


def test_cylindrical_geometry_with_inconsistent_detector_numbers_triggers_fallback(
        nxroot):
    var = sc.array(dims=['xx', 'yy'], unit='K', values=[[1.1], [3.3]])
    detector = nxroot.create_class('detector0', NXdetector)
    detector.create_field('data', var)
    detector.attrs['axes'] = ['xx', 'yy']
    detector.create_field('detector_numbers',
                          sc.array(dims=var.dims, values=[[1], [2]], unit=None))
    create_cylindrical_geometry_detector_numbers_1234(detector,
                                                      name='shape',
                                                      detector_numbers=True)
    loaded = detector[...]
    assert isinstance(loaded, sc.DataGroup)
    assert isinstance(loaded['shape'], sc.DataGroup)


def test_cylindrical_geometry_with_detector_numbers(nxroot):
    var = sc.array(dims=['xx', 'yy'], unit='K', values=[[1.1, 2.2], [3.3, 4.4]])
    detector = nxroot.create_class('detector0', NXdetector)
    detector.create_field('data', var)
    detector.attrs['axes'] = ['xx', 'yy']
    detector_number = sc.array(dims=var.dims, values=[[1, 2], [3, 4]], unit=None)
    detector.create_field('detector_number', detector_number)
    create_cylindrical_geometry_detector_numbers_1234(detector,
                                                      name='shape',
                                                      detector_numbers=True)
    loaded = detector[...]
    shape = loaded.coords['shape']
    assert shape.dims == detector_number.dims
    for i in [0, 3]:
        assert sc.identical(
            shape.values[i],
            sc.Dataset({
                'face1_center':
                sc.vectors(dims=['cylinder'], values=[[0, 0, 0]], unit='m'),
                'face1_edge':
                sc.vectors(dims=['cylinder'], values=[[0, 1, 0]], unit='m'),
                'face2_center':
                sc.vectors(dims=['cylinder'], values=[[3, 0, 0]], unit='m'),
            }))
    for i in [1, 2]:
        assert sc.identical(
            shape.values[i],
            sc.Dataset({
                'face1_center':
                sc.vectors(dims=['cylinder'], values=[[3, 0, 0]], unit='m'),
                'face1_edge':
                sc.vectors(dims=['cylinder'], values=[[0, 1, 0]], unit='m'),
                'face2_center':
                sc.vectors(dims=['cylinder'], values=[[0, 0, 0]], unit='m'),
            }))
