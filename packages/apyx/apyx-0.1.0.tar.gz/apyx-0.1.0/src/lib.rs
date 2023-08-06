use pyo3::prelude::*;
use apx::add;


#[pyfunction]
fn test(a: usize, b: usize) -> PyResult<String> {
    Ok(add(a, b).to_string())
}


#[pymodule]
fn apyx(_py: Python, m: &PyModule) -> PyResult<()> {
    m.add_function(wrap_pyfunction!(test, m)?)?;
    Ok(())
}
