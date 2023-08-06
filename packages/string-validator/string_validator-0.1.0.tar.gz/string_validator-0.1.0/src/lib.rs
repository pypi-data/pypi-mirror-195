use pyo3::prelude::*;

/// Validates whether the given string is an email based on the HTML5 spec. RFC 5322 is not practical in most circumstances and allows email addresses that are unfamiliar to most users.
#[pyfunction]
fn validate_email(val: &str) -> PyResult<bool> {
    Ok(validator::validate_email(val))
}

/// Validates whether the given string is an IP address.
#[pyfunction]
fn validate_ip(val: &str) -> PyResult<bool> {
    Ok(validator::validate_ip(val))
}

/// Validates whether the given string is an IPv4 address.
#[pyfunction]
fn validate_ipv4(val: &str) -> PyResult<bool> {
    Ok(validator::validate_ip_v4(val))
}

/// Validates whether the given string is an IPv6 address.
#[pyfunction]
fn validate_ipv6(val: &str) -> PyResult<bool> {
    Ok(validator::validate_ip_v6(val))
}

/// Validates whether the string given is an URL.
#[pyfunction]
fn validate_url(val: &str) -> PyResult<bool> {
    Ok(validator::validate_url(val))
}

#[pyfunction]
fn validate_credit_card(card: &str) -> PyResult<bool> {
    Ok(validator::validate_credit_card(card))
}

#[pyfunction]
fn validate_phone(phone_number: &str) -> PyResult<bool> {
    Ok(validator::validate_phone(phone_number))
}

#[pyfunction]
fn validate_non_control_character(alphabetic: &str) -> PyResult<bool> {
    Ok(validator::validate_non_control_character(alphabetic))
}

/// Creates a new CUID.
#[pyfunction]
fn create_cuid() -> PyResult<String> {
    Ok(cuid::cuid2())
}

#[pymodule]
fn string_validator(_py: Python, m: &PyModule) -> PyResult<()> {
    m.add_function(wrap_pyfunction!(validate_email, m)?)?;
    m.add_function(wrap_pyfunction!(validate_ip, m)?)?;
    m.add_function(wrap_pyfunction!(validate_ipv4, m)?)?;
    m.add_function(wrap_pyfunction!(validate_ipv6, m)?)?;
    m.add_function(wrap_pyfunction!(validate_url, m)?)?;
    m.add_function(wrap_pyfunction!(validate_credit_card, m)?)?;
    m.add_function(wrap_pyfunction!(validate_phone, m)?)?;
    m.add_function(wrap_pyfunction!(validate_non_control_character, m)?)?;
    m.add_function(wrap_pyfunction!(create_cuid, m)?)?;
    Ok(())
}
