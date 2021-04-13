extern crate pyo3;
extern crate pyo3_built;
extern crate svgbob;

mod built;

use pyo3::PyResult;
use pyo3::Python;
use pyo3::prelude::pymodule;
use pyo3::types::PyModule;
use pyo3::types::PyString;

#[cfg_attr(feature = "extension-module", pymodule(_svgbob))]
pub fn init(py: Python, m: &PyModule) -> PyResult<()> {
    m.add("__version__", env!("CARGO_PKG_VERSION"))?;
    m.add("__author__", env!("CARGO_PKG_AUTHORS").replace(':', "\n"))?;
    m.add("__build__", pyo3_built::pyo3_built!(py, built))?;

    #[pyfn(m, "to_svg")]
    fn to_svg_py(_py: Python, text: &PyString) -> PyResult<String> {
        text.to_str()
            .map(svgbob::to_svg)
            .map(|svg| svg.to_string())
    }

    Ok(())
}
