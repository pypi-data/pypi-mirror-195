use std::{
    fmt::Debug,
    hash::Hash,
    ops::{BitAnd, BitOr, Not},
    sync::Arc,
};

use num_bigint::BigUint;
use once_cell::sync::Lazy;
use rr_util::{
    name::Name,
    shape::Shape,
    tensor_util::{TorchDeviceDtype, TorchDeviceDtypeOp},
    util::{HashBytes, NamedAxes},
    IndexSet,
};

use crate::CircuitRc;

#[derive(Clone)]
pub struct CachedCircuitInfo {
    pub shape: Shape,
    pub flags: CircuitFlags,
    pub hash: HashBytes,
    pub device_dtype: TorchDeviceDtypeOp,
    pub named_axes: NamedAxes,
    pub free_symbols: Option<Arc<IndexSet<CircuitRc>>>, // always Symbols
    pub name: Option<Name>,
    pub children: Vec<CircuitRc>,
}

impl CachedCircuitInfo {
    // leaves some fields undefined/default for now... TODO move more stuff here
    pub fn incomplete(
        name: Option<Name>,
        shape: Shape,
        children: Vec<CircuitRc>,
    ) -> CachedCircuitInfo {
        CachedCircuitInfo {
            shape,
            flags: Default::default(),
            hash: Default::default(),
            device_dtype: Default::default(),
            named_axes: Default::default(),
            free_symbols: Default::default(),
            name,
            children,
        }
    }
}

#[derive(Clone, Copy, Hash, Debug, Eq, PartialEq)]
pub struct CircuitFlags(pub u8);
impl CircuitFlags {
    pub const IS_CONSTANT: CircuitFlags = CircuitFlags(0b0001);
    pub const IS_EXPLICITLY_COMPUTABLE: CircuitFlags = CircuitFlags(0b0010);
    pub const CAN_BE_SAMPLED: CircuitFlags = CircuitFlags(0b0100);
    pub const USE_AUTONAME: CircuitFlags = CircuitFlags(0b1000);

    pub const NONE: CircuitFlags = CircuitFlags(0b0);
    pub fn check(self, other: CircuitFlags) -> bool {
        (self & other).0 != 0
    }

    pub fn all_true() -> Self {
        CircuitFlags::IS_EXPLICITLY_COMPUTABLE
            | CircuitFlags::IS_CONSTANT
            | CircuitFlags::CAN_BE_SAMPLED
            | CircuitFlags::USE_AUTONAME
    }
}

impl Default for CircuitFlags {
    fn default() -> Self {
        Self::all_true()
    }
}

impl BitOr for CircuitFlags {
    type Output = CircuitFlags;
    fn bitor(self, rhs: Self) -> Self::Output {
        Self(self.0 | rhs.0)
    }
}
impl BitAnd for CircuitFlags {
    type Output = CircuitFlags;
    fn bitand(self, rhs: Self) -> Self::Output {
        Self(self.0 & rhs.0)
    }
}
use std::ops::BitOrAssign;
impl BitOrAssign for CircuitFlags {
    fn bitor_assign(&mut self, rhs: Self) {
        self.0 |= rhs.0
    }
}
use std::ops::BitAndAssign;
impl BitAndAssign for CircuitFlags {
    fn bitand_assign(&mut self, rhs: Self) {
        self.0 &= rhs.0
    }
}
impl Not for CircuitFlags {
    type Output = CircuitFlags;
    fn not(self) -> CircuitFlags {
        Self(!self.0)
    }
}

/// don't want to print hash with Debug; print selected fields
impl Debug for CachedCircuitInfo {
    fn fmt(&self, f: &mut std::fmt::Formatter<'_>) -> std::fmt::Result {
        write!(
            f,
            "{} {:?} {:?}",
            self.name.map_or("", |n| n.str()),
            self.shape,
            self.device_dtype,
        )
    }
}

impl CachedCircuitInfo {
    pub fn numel(&self) -> BigUint {
        self.shape
            .iter()
            .map(|x| BigUint::from(x.t().unwrap_or(1)))
            .product()
    }
    /// Saturating element count
    pub fn numel_usize(&self) -> usize {
        let numel_digits = self.numel().to_u64_digits();
        match numel_digits.len() {
            0 => 0,
            1 => numel_digits[0] as usize,
            _ => usize::MAX,
        }
    }

    pub fn naive_mem_use(&self, device_dtype: Option<TorchDeviceDtype>) -> BigUint {
        self.numel()
            * BigUint::from(
                device_dtype
                    .unwrap_or(self.device_dtype.unwrap_or_defaults())
                    .size(),
            )
    }
    // once we're scheduling everything is batch-realizeable so we don't need biguint
    pub fn naive_mem_use_usize(&self, device_dtype: Option<TorchDeviceDtype>) -> usize {
        self.numel_usize().saturating_mul(
            device_dtype
                .unwrap_or(self.device_dtype.unwrap_or_defaults())
                .size(),
        )
    }
    pub fn rank(&self) -> usize {
        self.shape.len()
    }
    pub fn hash_usize(&self) -> usize {
        let mut hash_prefix: [u8; 8] = Default::default();
        hash_prefix.copy_from_slice(&self.hash[..8]);
        usize::from_le_bytes(hash_prefix)
    }
    pub fn is_constant(&self) -> bool {
        self.flags.check(CircuitFlags::IS_CONSTANT)
    }
    pub fn can_be_sampled(&self) -> bool {
        self.flags.check(CircuitFlags::CAN_BE_SAMPLED)
    }
    pub fn is_explicitly_computable(&self) -> bool {
        self.flags.check(CircuitFlags::IS_EXPLICITLY_COMPUTABLE)
    }
    pub fn use_autoname(&self) -> bool {
        self.flags.check(CircuitFlags::USE_AUTONAME)
    }

    pub fn get_raw_free_symbols(&self) -> &IndexSet<CircuitRc> {
        static NULL_INDEX_SET: Lazy<IndexSet<CircuitRc>> = Lazy::new(|| IndexSet::default());
        if let Some(z) = &self.free_symbols {
            &**z
        } else {
            &*NULL_INDEX_SET
        }
    }
}
