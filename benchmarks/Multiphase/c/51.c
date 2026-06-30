int main(){
    int x, y, z;

    // pre-conditions
    x = 0;
    y = 3333;
    z = 6666;

    // loop body
    while(unknown()){
        if(y >= 6666){
            z = z + 1;
        }
        if(x >= 3333){
            y = y + 1;
        }
        x = x + 1;
    }

    // post-condition
    if(x == 9999){
        assert(z == x);
    }
    
}