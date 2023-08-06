use ::myco::gen_html;
use pyo3::prelude::*;
#[pymodule]
fn mycopython(_py: Python<'_>, m: &PyModule) -> PyResult<()> {
    m.add_function(wrap_pyfunction!(html, m)?)?;
    Ok(())
}

#[pyfunction]
fn html(str: &str) -> PyResult<String> {
    Ok(gen_html(str))
}
