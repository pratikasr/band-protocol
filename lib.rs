use obi::{OBIDecode, OBIEncode, OBISchema};
use owasm_kit::{execute_entry_point, ext, oei, prepare_entry_point};

#[derive(OBIDecode, OBISchema)]
struct Input {
    symbols: [String],
    multiplier: u64,
}

#[derive(OBIEncode, OBISchema)]
struct Output {
    rates: [u64],
}

const DATA_SOURCE_ID: i64 = 162;
const EXTERNAL_ID: i64 = 0;

#[no_mangle]
fn prepare_impl(input: Input) {
    oei::ask_external_data(
        DATA_SOURCE_ID,
        EXTERNAL_ID,
        format!("{} {}", input.symbols, input.multiplier).as_bytes(),
    );
}

#[no_mangle]
fn execute_impl(_input: Input) -> Output {
    Output {
        rates: ext::load_majority::<String>(EXTERNAL_ID).unwrap(),
    }
}

prepare_entry_point!(prepare_impl);
execute_entry_point!(execute_impl);
