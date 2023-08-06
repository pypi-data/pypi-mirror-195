import h5py
import numpy as np
import pytest
import scipp as sc

from scippnexus import (
    NXdetector,
    NXentry,
    NXlog,
    NXroot,
    NXtransformations,
    nxtransformations,
)


@pytest.fixture()
def nxroot():
    """Yield NXroot containing a single NXentry named 'entry'"""
    with h5py.File('dummy.nxs', mode='w', driver="core", backing_store=False) as f:
        root = NXroot(f)
        root.create_class('entry', NXentry)
        yield root


def create_detector(group):
    data = sc.array(dims=['xx', 'yy'], values=[[1.1, 2.2], [3.3, 4.4]])
    detector_numbers = sc.array(dims=['xx', 'yy'],
                                unit=None,
                                values=np.array([[1, 2], [3, 4]]))
    detector = group.create_class('detector_0', NXdetector)
    detector.create_field('detector_number', detector_numbers)
    detector.create_field('data', data)
    return detector


def test_Transformation_with_single_value(nxroot):
    detector = create_detector(nxroot)
    detector.create_field('depends_on', sc.scalar('/detector_0/transformations/t1'))
    transformations = detector.create_class('transformations', NXtransformations)
    value = sc.scalar(6.5, unit='mm')
    offset = sc.spatial.translation(value=[1, 2, 3], unit='mm')
    vector = sc.vector(value=[0, 0, 1])
    t = value.to(unit='m') * vector
    expected = sc.spatial.translations(dims=t.dims, values=t.values, unit=t.unit)
    expected = expected * sc.spatial.translation(value=[0.001, 0.002, 0.003], unit='m')
    value = transformations.create_field('t1', value)
    value.attrs['depends_on'] = '.'
    value.attrs['transformation_type'] = 'translation'
    value.attrs['offset'] = offset.values
    value.attrs['offset_units'] = str(offset.unit)
    value.attrs['vector'] = vector.value

    depends_on = detector['depends_on'][()]
    t = nxtransformations.Transformation(nxroot[depends_on])
    assert t.depends_on is None
    assert sc.identical(t.offset, offset)
    assert sc.identical(t.vector, vector)
    assert sc.identical(t[()], expected)


def test_chain_with_single_values_and_different_unit(nxroot):
    detector = create_detector(nxroot)
    detector.create_field('depends_on', sc.scalar('/detector_0/transformations/t1'))
    transformations = detector.create_class('transformations', NXtransformations)
    value = sc.scalar(6.5, unit='mm')
    offset = sc.spatial.translation(value=[1, 2, 3], unit='mm')
    vector = sc.vector(value=[0, 0, 1])
    t = value.to(unit='m') * vector
    value1 = transformations.create_field('t1', value)
    value1.attrs['depends_on'] = 't2'
    value1.attrs['transformation_type'] = 'translation'
    value1.attrs['offset'] = offset.values
    value1.attrs['offset_units'] = str(offset.unit)
    value1.attrs['vector'] = vector.value
    value2 = transformations.create_field('t2', value.to(unit='cm'))
    value2.attrs['depends_on'] = '.'
    value2.attrs['transformation_type'] = 'translation'
    value2.attrs['vector'] = vector.value

    expected = (sc.spatial.translations(dims=t.dims, values=2 * t.values, unit=t.unit) *
                sc.spatial.translation(value=[0.001, 0.002, 0.003], unit='m'))
    assert sc.identical(detector[...].coords['depends_on'], expected)


def test_Transformation_with_multiple_values(nxroot):
    detector = create_detector(nxroot)
    detector.create_field('depends_on', sc.scalar('/detector_0/transformations/t1'))
    transformations = detector.create_class('transformations', NXtransformations)
    log = sc.DataArray(
        sc.array(dims=['time'], values=[1.1, 2.2], unit='m'),
        coords={'time': sc.array(dims=['time'], values=[11, 22], unit='s')})
    log.coords['time'] = sc.epoch(unit='ns') + log.coords['time'].to(unit='ns')
    offset = sc.spatial.translation(value=[1, 2, 3], unit='m')
    vector = sc.vector(value=[0, 0, 1])
    t = log * vector
    t.data = sc.spatial.translations(dims=t.dims, values=t.values, unit=t.unit)
    expected = t * offset
    value = transformations.create_class('t1', NXlog)
    value['time'] = log.coords['time'] - sc.epoch(unit='ns')
    value['value'] = log.data
    value.attrs['depends_on'] = '.'
    value.attrs['transformation_type'] = 'translation'
    value.attrs['offset'] = offset.values
    value.attrs['offset_units'] = str(offset.unit)
    value.attrs['vector'] = vector.value

    depends_on = detector['depends_on'][()]
    t = nxtransformations.Transformation(nxroot[depends_on])
    assert t.depends_on is None
    assert sc.identical(t.offset, offset)
    assert sc.identical(t.vector, vector)
    assert sc.identical(t[()], expected)


def test_chain_with_multiple_values(nxroot):
    detector = create_detector(nxroot)
    detector.create_field('depends_on', sc.scalar('/detector_0/transformations/t1'))
    transformations = detector.create_class('transformations', NXtransformations)
    log = sc.DataArray(
        sc.array(dims=['time'], values=[1.1, 2.2], unit='m'),
        coords={'time': sc.array(dims=['time'], values=[11, 22], unit='s')})
    log.coords['time'] = sc.epoch(unit='ns') + log.coords['time'].to(unit='ns')
    offset = sc.spatial.translation(value=[1, 2, 3], unit='m')
    vector = sc.vector(value=[0, 0, 1])
    t = log * vector
    t.data = sc.spatial.translations(dims=t.dims, values=t.values, unit=t.unit)
    value1 = transformations.create_class('t1', NXlog)
    value1['time'] = log.coords['time'] - sc.epoch(unit='ns')
    value1['value'] = log.data
    value1.attrs['depends_on'] = 't2'
    value1.attrs['transformation_type'] = 'translation'
    value1.attrs['offset'] = offset.values
    value1.attrs['offset_units'] = str(offset.unit)
    value1.attrs['vector'] = vector.value
    value2 = transformations.create_class('t2', NXlog)
    value2['time'] = log.coords['time'] - sc.epoch(unit='ns')
    value2['value'] = log.data
    value2.attrs['depends_on'] = '.'
    value2.attrs['transformation_type'] = 'translation'
    value2.attrs['vector'] = vector.value

    expected = t * (t * offset)
    assert sc.identical(detector[...].coords['depends_on'].value, expected)


def test_chain_with_multiple_values_and_different_time_unit(nxroot):
    detector = create_detector(nxroot)
    detector.create_field('depends_on', sc.scalar('/detector_0/transformations/t1'))
    transformations = detector.create_class('transformations', NXtransformations)
    # Making sure to not use nanoseconds since that is used internally and may thus
    # mask bugs.
    log = sc.DataArray(
        sc.array(dims=['time'], values=[1.1, 2.2], unit='m'),
        coords={'time': sc.array(dims=['time'], values=[11, 22], unit='s')})
    log.coords['time'] = sc.epoch(unit='us') + log.coords['time'].to(unit='us')
    offset = sc.spatial.translation(value=[1, 2, 3], unit='m')
    vector = sc.vector(value=[0, 0, 1])
    t = log * vector
    t.data = sc.spatial.translations(dims=t.dims, values=t.values, unit=t.unit)
    value1 = transformations.create_class('t1', NXlog)
    value1['time'] = log.coords['time'] - sc.epoch(unit='us')
    value1['value'] = log.data
    value1.attrs['depends_on'] = 't2'
    value1.attrs['transformation_type'] = 'translation'
    value1.attrs['offset'] = offset.values
    value1.attrs['offset_units'] = str(offset.unit)
    value1.attrs['vector'] = vector.value
    value2 = transformations.create_class('t2', NXlog)
    value2['time'] = log.coords['time'].to(unit='ms') - sc.epoch(unit='ms')
    value2['value'] = log.data
    value2.attrs['depends_on'] = '.'
    value2.attrs['transformation_type'] = 'translation'
    value2.attrs['vector'] = vector.value

    expected = t * (t * offset)
    assert sc.identical(detector[...].coords['depends_on'].value, expected)


def test_broken_time_dependent_transformation_returns_path_and_transformations(nxroot):
    detector = create_detector(nxroot)
    detector.create_field('depends_on', sc.scalar('/detector_0/transformations/t1'))
    transformations = detector.create_class('transformations', NXtransformations)
    log = sc.DataArray(
        sc.array(dims=['time'], values=[1.1, 2.2], unit='m'),
        coords={'time': sc.array(dims=['time'], values=[11, 22], unit='s')})
    log.coords['time'] = sc.epoch(unit='ns') + log.coords['time'].to(unit='ns')
    offset = sc.spatial.translation(value=[1, 2, 3], unit='m')
    vector = sc.vector(value=[0, 0, 1])
    t = log * vector
    t.data = sc.spatial.translations(dims=t.dims, values=t.values, unit=t.unit)
    value = transformations.create_class('t1', NXlog)
    value['time'] = log.coords['time'] - sc.epoch(unit='ns')
    # This makes the transform "broken" since "time" has length 2 but data has length 0.
    value['value'] = log.data[0:0]
    value.attrs['depends_on'] = '.'
    value.attrs['transformation_type'] = 'translation'
    value.attrs['offset'] = offset.values
    value.attrs['offset_units'] = str(offset.unit)
    value.attrs['vector'] = vector.value

    loaded = detector[()]
    assert sc.identical(loaded.coords['depends_on'],
                        sc.scalar('/detector_0/transformations/t1'))
    t = loaded.coords['transformations'].value
    assert isinstance(t, sc.DataGroup)
    # Due to the way NXtransformations works, vital information is stored in the
    # attributes. DataGroup does currently not support attributes, so this information
    # is mostly useless until that is addressed.
    assert 't1' in t


def write_translation(group, name: str, value: sc.Variable, offset: sc.Variable,
                      vector: sc.Variable) -> None:
    dset = group.create_field(name, value)
    dset.attrs['transformation_type'] = 'translation'
    dset.attrs['offset'] = offset.values
    dset.attrs['offset_units'] = str(offset.unit)
    dset.attrs['vector'] = vector.value


def test_nxtransformations_group_single_item(nxroot):
    value = sc.scalar(2.4, unit='mm')
    offset = sc.spatial.translation(value=[6, 2, 6], unit='mm')
    vector = sc.vector(value=[0, 1, 1])
    t = value.to(unit='m') * vector
    expected = (sc.spatial.translations(dims=t.dims, values=t.values, unit=t.unit) *
                sc.spatial.translation(value=[0.006, 0.002, 0.006], unit='m'))

    transformations = nxroot.create_class('transformations', NXtransformations)
    write_translation(transformations, 't1', value, offset, vector)

    loaded = nxroot['transformations'][()]
    assert set(loaded.keys()) == {'t1'}
    assert sc.identical(loaded['t1'], expected)


def test_nxtransformations_group_two_independent_items(nxroot):
    transformations = nxroot.create_class('transformations', NXtransformations)

    value = sc.scalar(2.4, unit='mm')
    offset = sc.spatial.translation(value=[6, 2, 6], unit='mm')
    vector = sc.vector(value=[0, 1, 1])
    t = value.to(unit='m') * vector
    write_translation(transformations, 't1', value, offset, vector)
    expected1 = (sc.spatial.translations(dims=t.dims, values=t.values, unit=t.unit) *
                 sc.spatial.translation(value=[0.006, 0.002, 0.006], unit='m'))

    value = value * 0.1
    t = value.to(unit='m') * vector
    write_translation(transformations, 't2', value, offset, vector)
    expected2 = (sc.spatial.translations(dims=t.dims, values=t.values, unit=t.unit) *
                 sc.spatial.translation(value=[0.006, 0.002, 0.006], unit='m'))

    loaded = nxroot['transformations'][()]
    assert set(loaded.keys()) == {'t1', 't2'}
    assert sc.identical(loaded['t1'], expected1)
    assert sc.identical(loaded['t2'], expected2)


def test_nxtransformations_group_single_chain(nxroot):
    transformations = nxroot.create_class('transformations', NXtransformations)

    value = sc.scalar(2.4, unit='mm')
    offset = sc.spatial.translation(value=[6, 2, 6], unit='mm')
    vector = sc.vector(value=[0, 1, 1])
    t = value.to(unit='m') * vector
    write_translation(transformations, 't1', value, offset, vector)
    expected1 = (sc.spatial.translations(dims=t.dims, values=t.values, unit=t.unit) *
                 sc.spatial.translation(value=[0.006, 0.002, 0.006], unit='m'))

    value = value * 0.1
    t = value.to(unit='m') * vector
    write_translation(transformations, 't2', value, offset, vector)
    transformations['t2'].attrs['depends_on'] = 't1'
    expected2 = (expected1 *
                 sc.spatial.translations(dims=t.dims, values=t.values, unit=t.unit) *
                 sc.spatial.translation(value=[0.006, 0.002, 0.006], unit='m'))

    loaded = nxroot['transformations'][()]
    assert set(loaded.keys()) == {'t1', 't2'}
    assert sc.identical(loaded['t1'], expected1)
    assert sc.allclose(loaded['t2'], expected2)


def test_slice_transformations(nxroot):
    transformations = nxroot.create_class('transformations', NXtransformations)
    log = sc.DataArray(
        sc.array(dims=['time'], values=[1.1, 2.2, 3.3], unit='m'),
        coords={'time': sc.array(dims=['time'], values=[11, 22, 33], unit='s')})
    log.coords['time'] = sc.epoch(unit='ns') + log.coords['time'].to(unit='ns')
    offset = sc.spatial.translation(value=[1, 2, 3], unit='m')
    vector = sc.vector(value=[0, 0, 1])
    t = log * vector
    t.data = sc.spatial.translations(dims=t.dims, values=t.values, unit=t.unit)
    value1 = transformations.create_class('t1', NXlog)
    value1['time'] = log.coords['time'] - sc.epoch(unit='ns')
    value1['value'] = log.data
    value1.attrs['transformation_type'] = 'translation'
    value1.attrs['offset'] = offset.values
    value1.attrs['offset_units'] = str(offset.unit)
    value1.attrs['vector'] = vector.value

    expected = t * offset

    assert sc.identical(nxroot['transformations']['time', 1:3]['t1'], expected['time',
                                                                               1:3])
