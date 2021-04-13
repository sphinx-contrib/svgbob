extern crate pyo3;
extern crate pyo3_built;
extern crate svgbob;

mod built;

use pyo3::PyResult;
use pyo3::Python;
use pyo3::prelude::pymodule;
use pyo3::prelude::pyfunction;
use pyo3::wrap_pyfunction;
use pyo3::types::PyModule;

#[pyfunction(
    "*",
    font_size="14",
    font_family = "\"monospace\"",
    fill_color="\"black\"",
    background="\"white\"",
    stroke_color="\"black\"",
    stroke_width="2.0",
    scale="8.0",
    enhance_circuitries="true",
    include_backdrop="false",
    include_styles="true",
    include_defs="true"
)]
fn to_svg(
    _py: Python,
    text: &str,
    font_size: usize,
    font_family: &str,
    fill_color: &str,
    background: &str,
    stroke_color: &str,
    stroke_width: f32,
    scale: f32,
    enhance_circuitries: bool,
    include_backdrop: bool,
    include_styles: bool,
    include_defs: bool,
) -> PyResult<String> {
    let settings = {
        let mut s = svgbob::Settings::default();
        s.font_size = font_size;
        s.font_family = font_family.to_string();
        s.fill_color = fill_color.to_string();
        s.background = background.to_string();
        s.stroke_color = stroke_color.to_string();
        s.stroke_width = stroke_width;
        s.scale = scale;
        s.enhance_circuitries = enhance_circuitries;
        s.include_backdrop = include_backdrop;
        s.include_styles = include_styles;
        s.include_defs = include_defs;
        s
    };
    Ok(svgbob::to_svg_with_settings(text, &settings))
}

#[cfg_attr(feature = "extension-module", pymodule(_svgbob))]
pub fn init(py: Python, m: &PyModule) -> PyResult<()> {
    m.add("__version__", env!("CARGO_PKG_VERSION"))?;
    m.add("__author__", env!("CARGO_PKG_AUTHORS").replace(':', "\n"))?;
    m.add("__build__", pyo3_built::pyo3_built!(py, built))?;

    m.add_function(wrap_pyfunction!(to_svg, m)?)?;

    Ok(())
}
