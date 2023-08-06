from typing import Optional, List

from sqlalchemy.orm import Query

from cg.store.models import Family, Sample


def get_samples_associated_with_case(case_samples: Query, case_id: str, **kwargs) -> Query:
    """Return samples associated with a case."""
    return case_samples.filter(Family.internal_id == case_id)


def get_cases_associated_with_sample(case_samples: Query, sample_id: str, **kwargs) -> Query:
    """Return cases associated with a sample."""
    return case_samples.filter(Sample.internal_id == sample_id)


def get_cases_associated_with_sample_by_entry_id(
    case_samples: Query, sample_entry_id: int, **kwargs
) -> Query:
    """Return cases associated with a sample."""
    return case_samples.filter(Sample.id == sample_entry_id)


def apply_case_sample_filter(
    functions: List[str],
    case_samples: Query,
    case_id: Optional[str] = None,
    sample_entry_id: Optional[int] = None,
    sample_id: Optional[str] = None,
) -> Query:
    """Apply filtering functions to the sample queries and return filtered results."""
    filter_map = {
        "get_cases_associated_with_sample": get_cases_associated_with_sample,
        "get_cases_associated_with_sample_by_entry_id": get_cases_associated_with_sample_by_entry_id,
        "get_samples_associated_with_case": get_samples_associated_with_case,
    }
    for function in functions:
        case_samples: Query = filter_map[function](
            case_samples=case_samples,
            case_id=case_id,
            sample_entry_id=sample_entry_id,
            sample_id=sample_id,
        )
    return case_samples
