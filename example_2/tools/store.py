def store_result(proxy, profile_dir, profile):
    results = []
    results.append(f'Proxy:           {proxy}')
    results.append(f'Email:           {profile.get_email()}')
    results.append(f'eBay Password:   {profile.ebay_password}')

    file = open(profile_dir + '/result.txt', 'w', encoding='utf8')
    file.write('\n'.join(results))
    file.close()