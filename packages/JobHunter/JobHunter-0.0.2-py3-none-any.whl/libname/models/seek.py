from __future__ import annotations

from typing import Any, Dict, List, Optional, Union

from pydantic import BaseModel, Field


class AppConfig(BaseModel):
    language: Optional[str] = None
    zone: Optional[str] = None


class Variation(BaseModel):
    name: Optional[str] = None
    index: Optional[int] = None


class SplitView2(BaseModel):
    name: Optional[str] = None
    variation: Optional[Variation] = None
    num: Optional[int] = None


class Experiments(BaseModel):
    splitView2: Optional[SplitView2] = None


class FeatureFlags(BaseModel):
    branchBannerPreview: Optional[bool] = None
    isBranchEnabledFlag: Optional[bool] = None
    srpSplitView: Optional[bool] = None
    showRecentSearches: Optional[bool] = None
    retireDisplayAds: Optional[str] = None
    showCareerAdvicePromo: Optional[bool] = None
    showInfoBanner: Optional[bool] = None
    isUnifiedLocationsEnabled: Optional[bool] = None


class Jobdetails(BaseModel):
    fraudReport: Optional[Dict[str, Any]] = None
    jobPending: Optional[bool] = None
    result: Optional[Any] = None
    pageLoadedCount: Optional[int] = None
    personalised: Optional[Any] = None


class RecentSearches(BaseModel):
    searches: Optional[List] = None


class SRP(BaseModel):
    content: Optional[str] = None
    learningSnippet: Optional[str] = None


class JDP(BaseModel):
    content: Optional[str] = None
    learningSnippet: Optional[str] = None


class Lmis(BaseModel):
    SRP: Optional[SRP] = None
    JDP: Optional[JDP] = None


class Query(BaseModel):
    daterange: Optional[str] = None
    page: Optional[str] = None


class Location(BaseModel):
    url: Optional[str] = None
    locale: Optional[str] = None
    prevPathname: Optional[str] = None
    query: Optional[Query] = None
    pageNumber: Optional[int] = None
    isHomepage: Optional[bool] = None
    pageTitle: Optional[str] = None
    pathname: Optional[str] = None
    hostname: Optional[str] = None
    href: Optional[str] = None
    port: Optional[str] = None
    protocol: Optional[str] = None
    requestId: Optional[str] = None
    hash: Optional[str] = None


class Nudges(BaseModel):
    nudges: Optional[List] = None
    currentNudgeIndex: Optional[int] = None
    nudgePostError: Optional[bool] = None


class Summary(BaseModel):
    displayTotalCount: Optional[str] = None
    text: Optional[str] = None


class SearchParams(BaseModel):
    keywords: Optional[str] = None
    where: Optional[str] = None
    daterange: Optional[str] = None
    page: Optional[str] = None


class Advertiser(BaseModel):
    id: Optional[str] = None
    description: Optional[str] = None


class Strategies(BaseModel):
    jdpLogo: Optional[str] = None
    serpLogo: Optional[str] = None


class Logo(BaseModel):
    strategies: Optional[Strategies] = None


class Assets(BaseModel):
    logo: Optional[Logo] = None


class BrandingItem(BaseModel):
    id: Optional[str] = None
    assets: Optional[Assets] = None


class Classification(BaseModel):
    id: Optional[str] = None
    description: Optional[str] = None


class SeoHierarchyItem(BaseModel):
    contextualName: Optional[str] = None


class JobLocation(BaseModel):
    label: Optional[str] = None
    countryCode: Optional[str] = None
    seoHierarchy: Optional[List[SeoHierarchyItem]] = None


class Logo1(BaseModel):
    id: Optional[str] = None
    description: Optional[Any] = None


class Tags(BaseModel):
    mordor__flights: Optional[str] = None
    seek_chalice_experiments_splitView2: Optional[str] = Field(
        None, alias='seek:chalice:experiments:splitView2'
    )


class SolMetadata(BaseModel):
    searchRequestToken: Optional[str] = None
    token: Optional[str] = None
    jobId: Optional[str] = None
    section: Optional[str] = None
    sectionRank: Optional[int] = None
    jobAdType: Optional[str] = None
    tags: Optional[Tags] = None


class SubClassification(BaseModel):
    id: Optional[str] = None
    description: Optional[str] = None


class Job(BaseModel):
    advertiser: Optional[Advertiser] = None
    area: Optional[str] = None
    areaId: Optional[int] = None
    areaWhereValue: Optional[str] = None
    automaticInclusion: Optional[bool] = None
    branding: Optional[Union[str, BrandingItem]] = None
    bulletPoints: Optional[List[str]] = None
    classification: Optional[Classification] = None
    companyName: Optional[str] = None
    companyProfileStructuredDataId: Optional[int] = None
    displayType: Optional[str] = None
    listingDateDisplay: Optional[str] = None
    location: Optional[str] = None
    locationId: Optional[int] = None
    locationWhereValue: Optional[str] = None
    id: Optional[int] = None
    isPremium: Optional[bool] = None
    isStandOut: Optional[bool] = None
    jobLocation: Optional[JobLocation] = None
    listingDate: Optional[str] = None
    logo: Optional[Logo1] = None
    roleId: Optional[str] = None
    salary: Optional[str] = None
    solMetadata: Optional[SolMetadata] = None
    subClassification: Optional[SubClassification] = None
    suburb: Optional[str] = None
    suburbId: Optional[int] = None
    suburbWhereValue: Optional[str] = None
    teaser: Optional[str] = None
    title: Optional[str] = None
    tracking: Optional[str] = None
    workType: Optional[str] = None
    isPrivateAdvertiser: Optional[bool] = None
    locationMatch: Optional[str] = None
    is_applied: Optional[str] = None
    url: Optional[str] = None

    @property
    def get_job_post_link(self):
        return f'https://www.seek.com.au/job/{self.id}'


class Results1(BaseModel):
    isLoading: Optional[bool] = None
    isZeroResults: Optional[bool] = None
    summary: Optional[Summary] = None
    header: Optional[Any] = None
    suggestions: Optional[Any] = None
    hasHeaderBeforeJobs: Optional[str] = None
    searchParams: Optional[SearchParams] = None
    jobs: Optional[List[Job]] = None
    suburbs: Optional[List[str]] = None


class PaginationParameters(BaseModel):
    seekSelectAllPages: Optional[bool] = None
    hadPremiumListings: Optional[bool] = None


class SortModeItem(BaseModel):
    isActive: Optional[bool] = None
    name: Optional[str] = None
    value: Optional[str] = None


class RelatedSearch(BaseModel):
    keywords: Optional[str] = None
    totalJobs: Optional[int] = None
    type: Optional[str] = None


class JoraCrossLink(BaseModel):
    canCrossLink: Optional[bool] = None


class Location1(BaseModel):
    matched: Optional[bool] = None
    whereId: Optional[int] = None
    type: Optional[str] = None
    suburbType: Optional[str] = None
    description: Optional[str] = None
    stateDescription: Optional[str] = None
    locationId: Optional[int] = None
    locationDescription: Optional[str] = None
    areaId: Optional[int] = None
    areaDescription: Optional[str] = None
    suburbParentDescription: Optional[str] = None


class Tags1(BaseModel):
    mordor__flights: Optional[str] = None
    chalice_search_api_solId: Optional[str] = Field(
        None, alias='chalice-search-api:solId'
    )
    dt_sol_correlation_id: Optional[str] = None
    seek_chalice_experiments_splitView2: Optional[str] = Field(
        None, alias='seek:chalice:experiments:splitView2'
    )


class SolMetadata1(BaseModel):
    requestToken: Optional[str] = None
    token: Optional[str] = None
    keywords: Optional[str] = None
    sortMode: Optional[str] = None
    createdSince: Optional[str] = None
    locations: Optional[List[str]] = None
    locationDistance: Optional[int] = None
    pageSize: Optional[int] = None
    pageNumber: Optional[int] = None
    totalJobCount: Optional[int] = None
    tags: Optional[Tags1] = None


class Results(BaseModel):
    results: Optional[Results1] = None
    isLoading: Optional[bool] = None
    isError: Optional[bool] = None
    source: Optional[str] = None
    companySuggestion: Optional[str] = None
    locationWhere: Optional[str] = None
    title: Optional[str] = None
    totalCount: Optional[int] = None
    jobIds: Optional[List[str]] = None
    lastPage: Optional[int] = None
    paginationParameters: Optional[PaginationParameters] = None
    sortMode: Optional[List[SortModeItem]] = None
    solReferenceKeys: Optional[List] = None
    hidden: Optional[bool] = None
    relatedSearches: Optional[List[RelatedSearch]] = None
    canonicalCompany: Optional[str] = None
    joraCrossLink: Optional[JoraCrossLink] = None
    location: Optional[Location1] = None
    userQueryId: Optional[str] = None
    uniqueSearchToken: Optional[str] = None
    solMetadata: Optional[SolMetadata1] = None
    solMetadataString: Optional[str] = None
    isRadialFilterShown: Optional[bool] = None
    isRadialFilterNudgeShown: Optional[bool] = None


class SavedJobs(BaseModel):
    jobs: Optional[Dict[str, Any]] = None


class SaveSearch(BaseModel):
    savedSearches: Optional[Any] = None
    savedSearchesReady: Optional[bool] = None
    emailAddress: Optional[str] = None
    errorMessage: Optional[str] = None
    isSaved: Optional[bool] = None
    saveable: Optional[bool] = None
    status: Optional[str] = None


class Query1(BaseModel):
    keywords: Optional[str] = None
    where: Optional[str] = None
    daterange: Optional[str] = None
    page: Optional[str] = None


class RefineParams(BaseModel):
    keywords: Optional[str] = None
    where: Optional[str] = None
    daterange: Optional[str] = None
    worktype: Optional[str] = None


class WorktypeItem(BaseModel):
    label: Optional[str] = None
    value: Optional[str] = None
    isActive: Optional[bool] = None
    refineParams: Optional[RefineParams] = None


class RefineParams1(BaseModel):
    keywords: Optional[str] = None
    where: Optional[str] = None
    daterange: Optional[str] = None
    salarytype: Optional[str] = None


class Type(BaseModel):
    label: Optional[str] = None
    value: Optional[str] = None
    isActive: Optional[bool] = None
    refineParams: Optional[RefineParams1] = None


class RefineParams2(BaseModel):
    keywords: Optional[str] = None
    where: Optional[str] = None
    daterange: Optional[str] = None
    salarytype: Optional[str] = None
    salaryrange: Optional[str] = None


class FromItem(BaseModel):
    label: Optional[str] = None
    value: Optional[str] = None
    isActive: Optional[bool] = None
    refineParams: Optional[RefineParams2] = None


class RefineParams3(BaseModel):
    keywords: Optional[str] = None
    where: Optional[str] = None
    daterange: Optional[str] = None
    salarytype: Optional[str] = None
    salaryrange: Optional[str] = None


class ToItem(BaseModel):
    label: Optional[str] = None
    value: Optional[str] = None
    isActive: Optional[bool] = None
    refineParams: Optional[RefineParams3] = None


class Salary(BaseModel):
    types: Optional[List[Type]] = None
    from_: Optional[List[FromItem]] = Field(None, alias='from')
    to: Optional[List[ToItem]] = None


class RefineParams4(BaseModel):
    keywords: Optional[str] = None
    where: Optional[str] = None
    daterange: Optional[str] = None


class DateRangeItem(BaseModel):
    label: Optional[str] = None
    value: Optional[str] = None
    isActive: Optional[bool] = None
    refineParams: Optional[RefineParams4] = None


class RefineParams5(BaseModel):
    keywords: Optional[str] = None
    where: Optional[str] = None
    daterange: Optional[str] = None
    classification: Optional[str] = None


class ClassificationItem(BaseModel):
    label: Optional[str] = None
    value: Optional[str] = None
    isActive: Optional[bool] = None
    refineParams: Optional[RefineParams5] = None


class RefineParams6(BaseModel):
    keywords: Optional[str] = None
    where: Optional[str] = None
    daterange: Optional[str] = None
    sortmode: Optional[str] = None


class SortmodeItem(BaseModel):
    label: Optional[str] = None
    value: Optional[str] = None
    isActive: Optional[bool] = None
    refineParams: Optional[RefineParams6] = None


class RefineParams7(BaseModel):
    keywords: Optional[str] = None
    where: Optional[str] = None
    daterange: Optional[str] = None
    distance: Optional[str] = None


class DistanceItem(BaseModel):
    label: Optional[str] = None
    value: Optional[str] = None
    isActive: Optional[bool] = None
    refineParams: Optional[RefineParams7] = None


class Refinements(BaseModel):
    counts: Optional[str] = None
    worktype: Optional[List[WorktypeItem]] = None
    salary: Optional[Salary] = None
    dateRange: Optional[List[DateRangeItem]] = None
    classification: Optional[List[ClassificationItem]] = None
    sortmode: Optional[List[SortmodeItem]] = None
    distance: Optional[List[DistanceItem]] = None
    clear: Optional[Dict[str, Any]] = None


class Search(BaseModel):
    keywordsField: Optional[str] = None
    whereField: Optional[str] = None
    filtersExpanded: Optional[bool] = None
    query: Optional[Query1] = None
    lastQuery: Optional[Dict[str, Any]] = None
    hasLoadedCounts: Optional[bool] = None
    refinements: Optional[Refinements] = None


class Partners(BaseModel):
    canCrossLink: Optional[bool] = None


class Seo(BaseModel):
    metaDescription: Optional[str] = None
    canonicalUrl: Optional[str] = None
    partners: Optional[Partners] = None


class User(BaseModel):
    authenticated: Optional[str] = None
    maybeAuthenticatedViaLastKnownSolUserId: Optional[bool] = None
    firstName: Optional[str] = None
    emailAddress: Optional[str] = None
    userClientId: Optional[str] = None
    ingressTestHeaders: Optional[Dict[str, Any]] = None


class Ui(BaseModel):
    isPageLoaded: Optional[bool] = None


class JobSearchResultModel(BaseModel):
    appConfig: Optional[AppConfig] = None
    experiments: Optional[Experiments] = None
    featureFlags: Optional[FeatureFlags] = None
    jobdetails: Optional[Jobdetails] = None
    recentSearches: Optional[RecentSearches] = None
    lmis: Optional[Lmis] = None
    location: Optional[Location] = None
    nudges: Optional[Nudges] = None
    results: Optional[Results] = None
    savedJobs: Optional[SavedJobs] = None
    saveSearch: Optional[SaveSearch] = None
    search: Optional[Search] = None
    seo: Optional[Seo] = None
    user: Optional[User] = None
    ui: Optional[Ui] = None
    __redux_hotjar_state: Optional[List[List[str]]] = Field(
        None, alias='@@redux-hotjar-state'
    )
