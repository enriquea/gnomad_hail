from gnomad_hail.resources.resource_utils import (
    TableResource,
    VersionedTableResource,
    DataException,
)

CURRENT_EXOME_RELEASE = ""
CURRENT_GENOME_RELEASE = "3.0"
EXOME_RELEASES = []
GENOME_RELEASES = ["3.0"]
DATA_TYPES = ["genomes"]

GENOME_POPS = ["AFR", "AMI", "AMR", "ASJ", "EAS", "FIN", "NFE", "SAS", "OTH"]


def _public_release_ht_path(data_type: str, version: str) -> str:
    """
    Get public release table path

    :param str data_type: One of "exomes" or "genomes"
    :param str version: One of the release versions of gnomAD on GRCh38
    :return: Path to release Table
    :rtype: str
    """
    return f"gs://gnomad-public/release/{version}/ht/{data_type}/gnomad.{data_type}.r{version}.sites.ht"


def _public_coverage_ht_path(data_type: str, version: str) -> str:
    """
    Get public coverage hail table

    :param str data_type: One of "exomes" or "genomes"
    :param str version: One of the release versions of gnomAD on GRCh38
    :return: path to coverage Table
    :rtype: str
    """
    return f"gs://gnomad-public/release/{version}/coverage/{data_type}/gnomad.{data_type}.r{version}.coverage.ht"


def public_release(data_type: str) -> VersionedTableResource:
    """
    Retrieves publicly released versioned table resource

    :param str data_type: One of "exomes" or "genomes"
    :return: Release Table
    :rtype: VersionedTableResource
    """

    if data_type not in DATA_TYPES:
        raise DataException(f'{data_type} not in {DATA_TYPES}, please select a data type from {DATA_TYPES}')

    if data_type == "exomes":
        current_release = CURRENT_EXOME_RELEASE
        releases = EXOME_RELEASES
    else:
        current_release = CURRENT_GENOME_RELEASE
        releases = GENOME_RELEASES

    return VersionedTableResource(
        current_release,
        {release: TableResource(path=_public_release_ht_path(data_type, release)) for release in releases},
    )


def coverage(data_type: str) -> VersionedTableResource:
    """
    Retrieves gnomAD's coverage table by data_type

    :param str data_type: One of "exomes" or "genomes"
    :return: Coverage Table
    :rtype: VersionedTableResource
    """
    if data_type not in DATA_TYPES:
        raise DataException(f'{data_type} not in {DATA_TYPES}, please select a data type from {DATA_TYPES}')

    if data_type == "exomes":
        current_release = CURRENT_EXOME_RELEASE
        releases = EXOME_RELEASES
    else:
        current_release = CURRENT_GENOME_RELEASE
        releases = GENOME_RELEASES

    return VersionedTableResource(
        current_release,
        {release: TableResource(path=_public_coverage_ht_path(data_type, release)) for release in releases},
    )


def release_vcf_path(data_type: str, version: str, contig: str) -> str:
    """
    Publically released VCF. Provide specific contig, i.e. "chr20", to retrieve contig
    specific VCF

    :param str data_type: One of "exomes" or "genomes"
    :param str version: One of the release versions of gnomAD on GRCh37
    :param str contig: Single contig "chr1" to "chrY"
    :return: Path to VCF
    :rtype: str
    """
    contig = f".{contig}" if contig else ""
    return f"gs://gnomad-public/release/{version}/vcf/{data_type}/gnomad.{data_type}.r{version}.sites{contig}.vcf.bgz"
