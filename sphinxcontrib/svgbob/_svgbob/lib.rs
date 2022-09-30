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
use pyo3_built::pyo3_built;

#[pyfunction(
    "*",
    font_size="None",
    font_family = "None",
    fill_color="None",
    background_color="None",
    stroke_color="None",
    stroke_width="None",
    scale="None",
    enhance_circuitries="true",
    include_backdrop="false",
    include_styles="true",
    include_defs="true",
    merge_line_with_shapes="false",
)]
fn to_svg(
    _py: Python,
    text: &str,
    font_size: Option<usize>,
    font_family: Option<&str>,
    fill_color: Option<&str>,
    background_color: Option<&str>,
    stroke_color: Option<&str>,
    stroke_width: Option<f32>,
    scale: Option<f32>,
    enhance_circuitries: bool,
    include_backdrop: bool,
    include_styles: bool,
    include_defs: bool,
    merge_line_with_shapes: bool,
) -> PyResult<String> {
    let settings = {
        let mut s = svgbob::Settings::default();
        if let Some(fs) = font_size {
            s.font_size = fs;
        }
        if let Some(ff) = font_family {
            s.font_family = ff.to_string();
        }
        if let Some(fc) = fill_color {
            s.fill_color = fc.to_string();
        }
        if let Some(bg) = background_color {
            s.background = bg.to_string();
        }
        if let Some(sc) = stroke_color {
            s.stroke_color = sc.to_string();
        }
        if let Some(sw) = stroke_width {
            s.stroke_width = sw;
        }
        if let Some(sc) = scale {
            s.scale = sc;
        }
        s.enhance_circuitries = enhance_circuitries;
        s.include_backdrop = include_backdrop;
        s.include_styles = include_styles;
        s.include_defs = include_defs;
        s.merge_line_with_shapes = merge_line_with_shapes;
        s
    };
    Ok(svgbob::to_svg_with_settings(text, &settings))
}

#[cfg_attr(feature = "extension-module", pymodule)]
#[cfg_attr(feature = "extension-module", pyo3(name = "_svgbob"))]
pub fn init(py: Python, m: &PyModule) -> PyResult<()> {
    m.add("__version__", env!("CARGO_PKG_VERSION"))?;
    m.add("__author__", env!("CARGO_PKG_AUTHORS").replace(':', "\n"))?;
    m.add("__build__", pyo3_built!(py, built))?;

    m.add_function(wrap_pyfunction!(to_svg, m)?)?;

    Ok(())
}
