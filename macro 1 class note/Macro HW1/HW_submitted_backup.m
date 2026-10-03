% ECON*6020 Assignment 1: Canadian business cycle statistics, 1976Q1-2026Q2
T = readtable("Assignment1_data.xlsx", Sheet="Combined", VariableNamingRule="preserve");

% ---- the ten series straight out of the file ------------------------------
output      = T.chained_2017_dollars_seasonally_adjusted_at_annual_rates_gross_domestic_product_at_market_prices;

consumption = T.chained_2017_dollars_seasonally_adjusted_at_annual_rates_semi_durable_goods ...
            + T.chained_2017_dollars_seasonally_adjusted_at_annual_rates_non_durable_goods ...
            + T.chained_2017_dollars_seasonally_adjusted_at_annual_rates_services;

investment  = T.chained_2017_dollars_seasonally_adjusted_at_annual_rates_non_residential_structures_machinery_and_equipment;

govcons     = T.chained_2017_dollars_seasonally_adjusted_at_annual_rates_general_governments_final_consumption_expenditure;

govinv      = T.chained_2017_dollars_seasonally_adjusted_at_annual_rates_general_governments_gross_fixed_capital_formation;

exports     = T.chained_2017_dollars_seasonally_adjusted_at_annual_rates_exports_of_goods_and_services;

imports     = T.chained_2017_dollars_seasonally_adjusted_at_annual_rates_less_imports_of_goods_and_services;

hours       = T.hours_worked_v4391505_quarterly_sum_hours;

pop         = T.population_v1_persons;

exrate      = 100 * T.exchange_rate_v37426_to_2016_v111666275_from_2017_quarterly_average_cad_per_usd;

% ---- the four you build ---------------------------------------------------
netexports   = 1 + (exports - imports) ./ output;

productivity = output ./ hours;

nominalGDP   = T.current_prices_seasonally_adjusted_at_annual_rates_gross_domestic_product_at_market_prices;
price        = 100 * nominalGDP ./ output;

% ---- per-capita series: deflate the real quantities by population ----------
y  = output      ./ pop;   % real GDP per capita
c  = consumption ./ pop;   % consumption per capita
i  = investment  ./ pop;   % investment per capita
gc = govcons     ./ pop;   % gov't consumption expenditure per capita
gi = govinv      ./ pop;   % gov't investment expenditure per capita
ex = exports     ./ pop;   % exports per capita
im = imports     ./ pop;   % imports per capita
n  = hours       ./ pop;   % hours worked per capita

% ---- already scale-free, so no population deflation ------------------------
nx   = netexports;   % 1 + (X - M)/Y   (a ratio)
w    = productivity; % labour productivity = output/hours (population cancels)
pgdp = price;        % price = GDP deflator (an index)

% ---- vector fed into the HP filter -----------------------------------------
% hpfilter.m example order: [y,c,i,gc,gi,ex,im,nx,n,w,k,mpk,exrate,pgdp,cpi,r,1+r]
% here k & mpk are skipped, and cpi / r / 1+r are not part of this assignment
a = [y, c, i, gc, gi, ex, im, nx, n, w, exrate, pgdp];   % 202 x 12

% ---- date labels for the figures (grab them before the filter section) -----
q  = string(T.quarter);                                              % "1976Q1" ... "2026Q2"
ty = double(extractBefore(q,5)) + (double(extractAfter(q,"Q"))-1)/4; % decimal year axis

% ---- HP filter: the block from hpfilter.m, applied to our 'a' --------------
lambda = 1600;
[T,nvar] = size(a);                                   % T = number of periods
d = (1+6*lambda)*ones(T,1);
x = diag(d);
d = -4*lambda*ones(T-1,1);
x = x + diag(d,1) + diag(d,-1);
d = lambda*ones(T-2,1);
x = x + diag(d,2) + diag(d,-2);
x(1,1) = 1+lambda;
x(1,2) = -2*lambda;
x(2,1) = -2*lambda;
x(2,2) = 1+5*lambda;
x(T,T) = 1+lambda;
x(T-1,T) = -2*lambda;
x(T,T-1) = -2*lambda;
x(T-1,T-1) = 1+5*lambda;
hpmat = inv(x);                                       % matrix to apply HP filter
raw = log(a);                                         % raw = logged data series
hptrend = hpmat*raw;                                  % HP trend line
hpdata = raw - hptrend;                               % deviation from HP trend
vcv = (hpdata'*hpdata)/T;                             % variance-covariance matrix
var = sum(vcv .* eye(nvar,nvar));                     % variance (vector)
sd = sqrt(var)*100;                                   % std. deviation (vector)
corr = vcv ./ sqrt(var'*var);                         % corr (matrix)

% autocorrelation of output: a measure of persistence
yhp = hpdata(2:T,1);              % for periods 2:T
yhplag = hpdata(1:T-1,1);         % for periods 1:T-1
autoy = corrcoef(yhp, yhplag);

% ---- question 1: the statistics ---------------------------------------------
sd                    % standard deviation of each series (%)
corr(1,1:end)         % correlation of each series with output
corr(9,10)            % corr(hours worked, labour productivity) - filtered series

% ======================= question 2: GDP and price ==========================
% column 1 of raw/hptrend/hpdata is GDP per capita; column 12 is the price
% (GDP deflator). raw = logged series, hptrend = trend, hpdata = cycle.

% ---- 2a: per variable, data + trend on top, the cycle below ----------------
figure
subplot(2,1,1)
plot(ty, raw(:,1)); hold on
plot(ty, hptrend(:,1))
title("GDP per capita: data and HP trend"); legend("log data","HP trend","Location","northwest"); grid on
subplot(2,1,2)
plot(ty, 100*hpdata(:,1))
yline(0, ':'); grid on
title("GDP per capita: cycle"); xlabel("year"); ylabel("% from trend")
exportgraphics(gcf, "q2_gdp.png", "Resolution", 150)

figure
subplot(2,1,1)
plot(ty, raw(:,12)); hold on
plot(ty, hptrend(:,12))
title("Price (GDP deflator): data and HP trend"); legend("log data","HP trend","Location","northwest"); grid on
subplot(2,1,2)
plot(ty, 100*hpdata(:,12))
yline(0, ':'); grid on
title("Price (GDP deflator): cycle"); xlabel("year"); ylabel("% from trend")
exportgraphics(gcf, "q2_price.png", "Resolution", 150)

% ---- 2b/2c: turning points of the three recessions -------------------------
% in each window: the last cycle peak = start of the recession, the trough =
% start of the recovery; depth and peak-to-trough quarters measure severity
cyc = 100*hpdata(:,1);                % GDP cycle, %

% early 1980s
win = find(ty >= 1980 & ty <= 1984);
[pk, a1] = max(cyc(win));  [tr, b1] = min(cyc(win));
fprintf("early 1980s:     peak %s (%+.2f%%)  trough %s (%+.2f%%)  %d quarters\n", ...
        q(win(a1)), pk, q(win(b1)), tr, win(b1) - win(a1));

% early 1990s
win = find(ty >= 1987 & ty <= 1993);
[pk, a1] = max(cyc(win));  [tr, b1] = min(cyc(win));
fprintf("early 1990s:     peak %s (%+.2f%%)  trough %s (%+.2f%%)  %d quarters\n", ...
        q(win(a1)), pk, q(win(b1)), tr, win(b1) - win(a1));

% Great Recession
win = find(ty >= 2007 & ty <= 2011);
[pk, a1] = max(cyc(win));  [tr, b1] = min(cyc(win));
fprintf("Great Recession: peak %s (%+.2f%%)  trough %s (%+.2f%%)  %d quarters\n", ...
        q(win(a1)), pk, q(win(b1)), tr, win(b1) - win(a1));

% stricter "recovery" reading: first quarter back at/above trend afterwards
win = find(ty >= 2007 & ty <= 2011);
[~, b1] = min(cyc(win));
back = find(cyc(win(b1):end) >= 0, 1);
fprintf("first quarter back at/above trend: %s\n", q(win(b1) + back - 1));

% ======================= question 3: cause ==================================
% evidence: the price cycle also falls below trend during the recession
% (output down and price down = demand shock, not a supply shock)
pc = 100*hpdata(:,12);                    % price cycle, %
win = find(ty >= 2008 & ty <= 2010.75);
[lo, m1] = min(pc(win));
fprintf("price cycle minimum 2008-2010: %+.2f%% in %s\n", lo, q(win(m1)));

% ======================= question 4: coronavirus ============================
% the hit: % change from 2019Q4 (last quarter before the pandemic) to the
% 2020Q2 trough, the cycle low within 2020, and when each series got back
% to its 2019Q4 level
cols  = [1 12 9];                     % output, price, hours worked
names = ["output", "price", "hours"];
k19 = find(q == "2019Q4");            % last pre-pandemic quarter
k20 = find(q == "2020Q2");            % pandemic trough quarter
for cc = 1:3
    k = cols(cc);
    win = find(ty >= 2020 & ty <= 2020.75);             % the four 2020 quarters
    [lo, m1] = min(hpdata(win,k));                      % cycle low within 2020
    back = k20 - 1 + find(raw(k20:end,k) >= raw(k19,k), 1);
    fprintf("%-7s: %+.1f%% (2019Q4 to 2020Q2), cycle low %+.1f%% in %s, back at 2019Q4 level: %s\n", ...
            names(cc), 100*(raw(k20,k) - raw(k19,k)), 100*lo, q(win(m1)), q(back));
end
