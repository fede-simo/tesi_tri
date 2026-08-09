test('checks_late_buy_orders', function (int $remainingQty, int $days, ?int $threshold, int $expectedCount) {

    $user = User::factory()->create();

    $buyOrder = BuyOrder::factory()->create();

    AlertSetting::factory()->create([
        'rule_name' => 'late_buy_orders',
        'user_id' => $user->id,
        'rule_params' => [
            'min_time_threshold' => $threshold,
        ],
    ]);

    BuyOrderArticle::factory()->create([
        'buy_order_id' => $buyOrder->id,
        'remaining_qty' => $remainingQty,
        'requested_delivery_date' => now()->addDays($days),
    ]);

    $result = app(LateBuyOrdersRule::class)->check($user);

    expect($result->count())->toBe($expectedCount);

})->with([
    [10, -1, 30, 1],    // scaduto ieri
    [0, -1, 30, 0],     // scaduto ieri ma con tutto consegnato
    [10, -40, 30, 0],   // scaduto 40gg fa
    [10, -20, 30, 1],   // scaduto 20gg fa
    [10, 1, 30, 0],     // scade domani
    [10, 0, null, 0],   // scade oggi
    [10, -30, 0, 0],    // scaduto 30 gg fa ma vengono presi solo quelli negli ultimi 0 giorni
]);