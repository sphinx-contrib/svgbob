mod built;

use pyo3::prelude::*;

use pyo3::types::PyModule;
use pyo3::wrap_pyfunction;
use pyo3::PyResult;
use pyo3::Python;
use pyo3_built::pyo3_built;

#[pyfunction]
#[pyo3(signature = (
    text,
    font_size=None,
    font_family = None,
    fill_color=None,
    background_color=None,
    stroke_color=None,
    stroke_width=None,
    scale=None,
    include_backdrop=false,
    include_styles=true,
    include_defs=true,
))]
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
    include_backdrop: bool,
    include_styles: bool,
    include_defs: bool,
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
        s.include_backdrop = include_backdrop;
        s.include_styles = include_styles;
        s.include_defs = include_defs;
        s
    };
    Ok(svgbob::to_svg_with_settings(text, &settings))
}

#[pymodule(name = "_svgbob")]
pub fn init(py: Python, m: &Bound<'_, PyModule>) -> PyResult<()> {
    m.add("__version__", env!("CARGO_PKG_VERSION"))?;
    m.add("__author__", env!("CARGO_PKG_AUTHORS").replace(':', "\n"))?;
    #[allow(deprecated)] // pyo3-built needs an update
    m.add("__build__", pyo3_built!(py, built))?;

    m.add_function(wrap_pyfunction!(to_svg, m)?)?;

    Ok(())
}
