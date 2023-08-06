import logging
from datetime import datetime
from dateutil.relativedelta import relativedelta
from krxmarket import fnltt_singl_acnt_all
from krxmarket.common.exception import NoDataReceived


LOGGER = logging.getLogger(__name__)


def _fv(item: dict, key: str):
    value = item.get(key)
    return value


def get_performance(
    corp_code: str,
    start_year: int,
    db_latest: str = ''
) -> list:
    """
    json structure
    [
        {
            year: '2016',
            quarter: 1,
            rcept_no: xxxxxxxx
            data: {
                CF: [
                    {},
                    {}
                ],
                IS: {
                
                }
            }
        }
    ]
    """
    year = start_year
    current = datetime.now()
    # 1분기보고서:11013, 반기보고서:11012, 3분기보고서:11014, 사업보고서 : 11011
    report_seq = ['11013', '11012', '11014', '11011']
    report_all = []
    if len(db_latest) < 5:
        db_latest = 20154  # 2015 q4
    else:
        db_latest = int(db_latest)

    while year <= current.year:
        for i, seq in enumerate(report_seq):
            # 2023 년 1분기 = 2023 / 3 / 1 + 1 month, 4월 1일
            # 현재가 4월 1일이 지나지 않으면 skip
            expected_end_day = datetime(year, (i + 1) * 3, 1) + relativedelta(months=1)
            if current < expected_end_day:
                continue
            elif int(str(year) + str(i + 1)) <= db_latest:
                continue

            result = {
                'year': str(year),
                'quarter': str(i + 1),
                'rcept_no': '',
                'data': {}
            }
            
            report = None
            try:
                report = fnltt_singl_acnt_all(corp_code, str(year), seq, 'CFS')
            except NoDataReceived:
                LOGGER.warning('no data CFS %d, quarter: %d', year, i + 1)
            
            if report is None:
                try:
                    report = fnltt_singl_acnt_all(corp_code, str(year), seq, 'OFS')
                except NoDataReceived:
                    LOGGER.warning('both CFS and OFS not exist %d, quarter: %d', year, i + 1)
                    continue

            if report['status'] == '000' and 'list' in report:
                items = _fv(report, 'list')
                for item in items:
                    sj_div = _fv(item, 'sj_div')
                    if sj_div not in result['data']:
                        result['data'][sj_div] = []
                    
                    if len(result['rcept_no']) == 0 and 'rcept_no' in item:
                        result['rcept_no'] = _fv(item, 'rcept_no')

                    result['data'][sj_div].append({
                        'account_nm': _fv(item, 'account_nm'),
                        'frmtrm_amount': _fv(item, 'frmtrm_amount'),
                        'thstrm_amount': _fv(item, 'thstrm_amount'),
                        'account_id': _fv(item, 'account_id')
                    })
                
            report_all.append(result)
        year += 1

    return report_all


if __name__ == '__main__':
    json_content = get_performance('00126380', 2023)
    import json
    with open('data.json', 'w') as f:
        json.dump(json_content, f)

